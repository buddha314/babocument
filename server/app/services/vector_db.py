"""
Vector Database Service

ChromaDB wrapper for semantic search and document storage.
Uses sentence-transformers/all-MiniLM-L6-v2 for embeddings.
"""

import structlog
from pathlib import Path
from typing import Any

import chromadb
from chromadb.config import Settings as ChromaSettings
from chromadb.utils import embedding_functions

from app.config import settings

logger = structlog.get_logger(__name__)


class VectorDatabase:
    """
    Vector database client for semantic search.
    
    Uses ChromaDB with persistent storage and sentence-transformers
    for embedding generation.
    """

    def __init__(self, storage_path: str | None = None):
        """
        Initialize ChromaDB client.
        
        Args:
            storage_path: Path to ChromaDB storage directory.
                         Defaults to config.chroma_persist_directory.
        """
        self.storage_path = Path(storage_path or settings.chroma_persist_directory)
        self.storage_path.mkdir(parents=True, exist_ok=True)

        logger.info(
            "initializing_vector_database",
            storage_path=str(self.storage_path),
            embedding_model=settings.embedding_model,
        )

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(self.storage_path),
            settings=ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True,
            ),
        )

        # Set up embedding function
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=settings.embedding_model
        )

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="research_papers",
            embedding_function=self.embedding_fn,  # type: ignore
            metadata={"description": "Research papers corpus for semantic search"},
        )

        logger.info(
            "vector_database_initialized",
            collection_name="research_papers",
            paper_count=self.collection.count(),
        )

    def add_papers(self, papers: list[dict[str, Any]]) -> int:
        """
        Add papers to vector database.
        
        Args:
            papers: List of paper dictionaries with keys:
                   - id: Unique paper identifier
                   - title: Paper title
                   - abstract: Paper abstract
                   - full_text: Full paper text (optional)
                   - authors: List of author names (optional)
                   - year: Publication year (optional)
                   - source: Data source (e.g., 'local', 'pubmed')
                   - doi: DOI identifier (optional)
                   - arxiv_id: arXiv identifier (optional)
        
        Returns:
            Number of papers added
        """
        if not papers:
            logger.warning("no_papers_to_add")
            return 0

        logger.info("adding_papers_to_vector_db", count=len(papers))

        try:
            # Prepare data for ChromaDB
            documents = [self._prepare_text(p) for p in papers]
            metadatas = [self._extract_metadata(p) for p in papers]
            ids = [str(p["id"]) for p in papers]

            # Add to collection
            self.collection.add(
                documents=documents,
                metadatas=metadatas,  # type: ignore
                ids=ids,
            )

            logger.info("papers_added_successfully", count=len(papers))
            return len(papers)

        except Exception as e:
            logger.error("error_adding_papers", error=str(e))
            raise

    def search(
        self,
        query: str,
        n_results: int = 10,
        filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Semantic search for papers.
        
        Args:
            query: Search query text
            n_results: Maximum number of results to return
            filters: Optional filters:
                    - year_min: Minimum publication year
                    - year_max: Maximum publication year
                    - source: Data source filter
                    - authors: Author name filter
        
        Returns:
            List of search results with similarity scores
        """
        logger.info(
            "searching_vector_db",
            query=query[:100],
            n_results=n_results,
            filters=filters,
        )

        try:
            # Build where clause
            where = self._build_filters(filters) if filters else None

            # Perform search
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where,
                include=["documents", "metadatas", "distances"],
            )

            # Format results
            formatted = self._format_results(results)

            logger.info("search_completed", results_count=len(formatted))
            return formatted

        except Exception as e:
            logger.error("search_error", error=str(e))
            raise

    def find_similar(
        self, paper_id: str, n_results: int = 10
    ) -> list[dict[str, Any]]:
        """
        Find papers similar to a given paper.
        
        Args:
            paper_id: ID of the reference paper
            n_results: Maximum number of similar papers to return
        
        Returns:
            List of similar papers with similarity scores
        """
        logger.info("finding_similar_papers", paper_id=paper_id, n_results=n_results)

        try:
            # Get the paper's embedding
            paper = self.collection.get(
                ids=[str(paper_id)],
                include=["embeddings"],
            )

            # Check if paper exists and has embeddings
            if not paper["ids"] or paper["embeddings"] is None or len(paper["embeddings"]) == 0:  # type: ignore
                logger.warning("paper_not_found", paper_id=paper_id)
                return []

            # Query with the paper's embedding
            results = self.collection.query(
                query_embeddings=[paper["embeddings"][0]],  # type: ignore
                n_results=n_results + 1,  # +1 to account for self
                include=["documents", "metadatas", "distances"],
            )

            # Format and filter out the source paper
            formatted = self._format_results(results, exclude_id=str(paper_id))

            logger.info("similar_papers_found", count=len(formatted))
            return formatted

        except Exception as e:
            logger.error("find_similar_error", error=str(e), paper_id=paper_id)
            raise

    def get_paper(self, paper_id: str) -> dict[str, Any] | None:
        """
        Retrieve a single paper by ID.
        
        Args:
            paper_id: Paper identifier
        
        Returns:
            Paper data or None if not found
        """
        try:
            result = self.collection.get(
                ids=[str(paper_id)],
                include=["documents", "metadatas"],
            )

            if not result["ids"]:
                return None

            return {
                "id": result["ids"][0],
                "document": result["documents"][0] if result["documents"] else "",
                "metadata": result["metadatas"][0] if result["metadatas"] else {},
            }

        except Exception as e:
            logger.error("get_paper_error", error=str(e), paper_id=paper_id)
            raise

    def delete_paper(self, paper_id: str) -> bool:
        """
        Delete a paper from the database.
        
        Args:
            paper_id: Paper identifier
        
        Returns:
            True if deleted, False if not found
        """
        try:
            self.collection.delete(ids=[str(paper_id)])
            logger.info("paper_deleted", paper_id=paper_id)
            return True

        except Exception as e:
            logger.error("delete_paper_error", error=str(e), paper_id=paper_id)
            raise

    def get_stats(self) -> dict[str, Any]:
        """
        Get database statistics.
        
        Returns:
            Dictionary with stats: total_papers, embedding_model, etc.
        """
        return {
            "total_papers": self.collection.count(),
            "embedding_model": settings.embedding_model,
            "embedding_dimension": 384,  # all-MiniLM-L6-v2
            "storage_path": str(self.storage_path),
            "collection_name": "research_papers",
        }

    def reset(self) -> None:
        """
        Reset the database (delete all papers).
        
        Warning: This is destructive and cannot be undone.
        """
        logger.warning("resetting_vector_database")
        self.client.delete_collection(name="research_papers")
        self.collection = self.client.create_collection(
            name="research_papers",
            embedding_function=self.embedding_fn,  # type: ignore
            metadata={"description": "Research papers corpus for semantic search"},
        )
        logger.info("vector_database_reset_complete")

    # Private helper methods

    def _prepare_text(self, paper: dict[str, Any]) -> str:
        """
        Prepare paper text for embedding generation.
        
        Combines title, abstract, and full text with weighting.
        Title and abstract are duplicated for higher importance.
        """
        title = paper.get("title", "")
        abstract = paper.get("abstract", "")
        body = paper.get("full_text", "")

        # Truncate body to avoid overwhelming the embedding
        if len(body) > 2000:
            body = body[:2000]

        # Weight title and abstract more heavily
        # This improves relevance for title/abstract matches
        combined = f"{title} {title} {abstract} {abstract} {body}"

        return combined.strip()

    def _extract_metadata(self, paper: dict[str, Any]) -> dict[str, Any]:
        """
        Extract metadata for filtering and display.
        
        ChromaDB requires all metadata values to be strings, numbers, or bools.
        """
        metadata = {
            "title": paper.get("title", ""),
            "source": paper.get("source", "unknown"),
        }

        # Add optional fields if present
        if "authors" in paper:
            # Join authors list into comma-separated string
            authors = paper["authors"]
            if isinstance(authors, list):
                metadata["authors"] = ", ".join(authors)
            else:
                metadata["authors"] = str(authors)

        if "year" in paper:
            metadata["year"] = int(paper["year"])

        if "doi" in paper:
            metadata["doi"] = str(paper["doi"])

        if "arxiv_id" in paper:
            metadata["arxiv_id"] = str(paper["arxiv_id"])

        if "file_path" in paper:
            metadata["file_path"] = str(paper["file_path"])

        return metadata

    def _build_filters(self, filters: dict[str, Any]) -> dict[str, Any] | None:
        """
        Build ChromaDB where clause from filter dictionary.
        
        Supports:
        - year_min/year_max: Year range filtering
        - source: Exact source match
        - authors: Author name contains (not supported by ChromaDB directly)
        """
        where: dict[str, Any] = {}

        if "year_min" in filters:
            where["year"] = {"$gte": int(filters["year_min"])}

        if "year_max" in filters:
            if "year" in where:
                where["year"]["$lte"] = int(filters["year_max"])
            else:
                where["year"] = {"$lte": int(filters["year_max"])}

        if "source" in filters:
            where["source"] = filters["source"]

        return where if where else None

    def _format_results(
        self,
        results: Any,
        exclude_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Format ChromaDB results into a standard structure.
        
        Converts distances to similarity scores (1 - distance).
        Optionally excludes a specific paper ID.
        """
        formatted = []

        # ChromaDB returns lists of lists (batch results)
        # We only query one at a time, so take first batch
        ids = results["ids"][0]
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for i in range(len(ids)):
            paper_id = ids[i]

            # Skip excluded paper
            if exclude_id and paper_id == exclude_id:
                continue

            # Convert distance to similarity (0-1 scale, higher is better)
            # ChromaDB uses squared L2 distance by default
            # Convert to similarity: 1 / (1 + distance)
            # This ensures similarity is always in [0, 1] range
            distance = distances[i]
            similarity = 1 / (1 + distance)

            formatted.append({
                "id": paper_id,
                "similarity": float(similarity),
                "document": documents[i],
                "metadata": metadatas[i],
            })

        return formatted


# Singleton instance for application-wide use
_vector_db_instance: VectorDatabase | None = None


def get_vector_db() -> VectorDatabase:
    """
    Get or create the global VectorDatabase instance.
    
    Returns:
        VectorDatabase singleton instance
    """
    global _vector_db_instance

    if _vector_db_instance is None:
        _vector_db_instance = VectorDatabase()

    return _vector_db_instance
