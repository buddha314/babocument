# Vector Database Selection Decision

**Decision Status:** ✅ RECOMMENDED - ChromaDB
**Date:** 2025-11-06
**Context:** Issue #4

## Executive Summary

**Recommendation:** Use **ChromaDB** with **Sentence Transformers** (all-MiniLM-L6-v2) for local vector storage and semantic search.

## Decision

**Selected:** ChromaDB with sentence-transformers/all-MiniLM-L6-v2

**Rationale:**
1. **Easiest setup** - `pip install chromadb` (no separate server)
2. **Python-native** - Perfect integration with FastAgent backend
3. **Local-first** - Configurable storage paths per developer
4. **Embedded** - Runs in-process, no Docker required
5. **Cost** - Completely free, no API costs
6. **Performance** - Sufficient for 100k+ documents
7. **Migration path** - Can upgrade to Weaviate/Qdrant later

## Architecture

```python
Research Agent → Vector DB Client → ChromaDB (local storage)
                                  ↓
                         Sentence Transformers
                         (all-MiniLM-L6-v2)
```

## Configuration

### Storage Structure
```
server/data/
└── chroma/
    ├── chroma.sqlite3
    └── embeddings/
```

### Environment Variables
```bash
DATA_DIR=/Users/developer/babocument_data
VECTOR_DB_PROVIDER=chroma
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### Python Configuration
```python
import chromadb
from chromadb.utils import embedding_functions

# Initialize client
client = chromadb.PersistentClient(
    path="./data/chroma"
)

# Set up embedding function
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Create collection
collection = client.get_or_create_collection(
    name="research_papers",
    embedding_function=embedding_fn
)
```

## Embedding Strategy

### Selected Model: all-MiniLM-L6-v2

**Specifications:**
- **Dimension:** 384
- **Speed:** ~3000 sentences/sec on CPU
- **Size:** 80MB
- **Quality:** Good for general text
- **Cost:** Free (local inference)

**Alternatives considered:**
- `all-mpnet-base-v2` - Better quality (768dim), slower
- `text-embedding-3-small` (OpenAI) - Excellent quality, $0.02/1M tokens
- `allenai/specter2` - Scientific paper specialist

**Why all-MiniLM-L6-v2:**
- Fast enough for real-time search
- Good balance of quality vs speed
- Small model size (quick download)
- Well-tested and reliable
- Free for development

## Comparison Matrix

| Database | Setup | Local | Python | Performance | Decision |
|----------|-------|-------|--------|-------------|----------|
| **Chroma** | ⭐⭐⭐⭐⭐ | ✅ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ **Selected** |
| Weaviate | ⭐⭐ | ✅ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Production option |
| Qdrant | ⭐⭐⭐ | ✅ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Alternative |
| Pinecone | ⭐⭐⭐⭐ | ❌ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Cloud-only |
| Milvus | ⭐ | ⚠️ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Too complex |

## Implementation Example

### Vector Database Client

```python
# server/app/services/vector_db.py
import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings

class VectorDatabase:
    def __init__(self, storage_path: str = "./data/chroma"):
        self.client = chromadb.PersistentClient(
            path=storage_path,
            settings=Settings(anonymized_telemetry=False)
        )

        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )

        self.collection = self.client.get_or_create_collection(
            name="research_papers",
            embedding_function=self.embedding_fn,
            metadata={"description": "Research papers corpus"}
        )

    def add_papers(self, papers: list[dict]):
        """Add papers to vector database"""
        self.collection.add(
            documents=[self._prepare_text(p) for p in papers],
            metadatas=[self._extract_metadata(p) for p in papers],
            ids=[p["id"] for p in papers]
        )

    def search(self, query: str, n_results: int = 10, filters: dict = None):
        """Semantic search for papers"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=self._build_filters(filters) if filters else None
        )
        return self._format_results(results)

    def find_similar(self, paper_id: str, n_results: int = 10):
        """Find papers similar to given paper"""
        results = self.collection.get(ids=[paper_id], include=["embeddings"])
        if not results["embeddings"]:
            return []

        similar = self.collection.query(
            query_embeddings=[results["embeddings"][0]],
            n_results=n_results + 1  # +1 to exclude self
        )

        # Filter out the source paper
        return self._format_results(similar, exclude_id=paper_id)

    def _prepare_text(self, paper: dict) -> str:
        """Prepare paper text for embedding"""
        title = paper.get("title", "")
        abstract = paper.get("abstract", "")
        body = paper.get("full_text", "")[:2000]

        # Weight title and abstract more
        return f"{title} {title} {abstract} {abstract} {body}"

    def _extract_metadata(self, paper: dict) -> dict:
        """Extract metadata for filtering"""
        return {
            "title": paper.get("title"),
            "authors": ",".join(paper.get("authors", [])),
            "year": paper.get("year"),
            "source": paper.get("source"),
            "arxiv_id": paper.get("arxiv_id"),
            "doi": paper.get("doi")
        }

    def _build_filters(self, filters: dict) -> dict:
        """Build Chroma where clause from filters"""
        where = {}
        if "year_min" in filters:
            where["year"] = {"$gte": filters["year_min"]}
        if "year_max" in filters:
            where.setdefault("year", {})["$lte"] = filters["year_max"]
        if "source" in filters:
            where["source"] = filters["source"]
        return where

    def _format_results(self, results, exclude_id: str = None) -> list[dict]:
        """Format Chroma results"""
        formatted = []
        for i in range(len(results["ids"][0])):
            paper_id = results["ids"][0][i]
            if exclude_id and paper_id == exclude_id:
                continue

            formatted.append({
                "id": paper_id,
                "similarity": 1 - results["distances"][0][i],
                "metadata": results["metadatas"][0][i]
            })
        return formatted
```

### Integration with Research Agent

```python
# server/app/agents/research.py
class ResearchAgent(BaseAgent):
    def __init__(self, redis_client, vector_db: VectorDatabase):
        super().__init__(redis_client)
        self.vector_db = vector_db

    async def search(self, query: str, filters: dict, task_id: str):
        await self.publish_progress(task_id, 20, "Searching vector database...")

        # Semantic search
        vector_results = self.vector_db.search(
            query=query,
            n_results=50,
            filters=filters
        )

        await self.publish_progress(task_id, 50, f"Found {len(vector_results)} papers...")

        # Rank and filter results
        ranked = self._rank_results(vector_results, query)

        return {
            "task_id": task_id,
            "results": ranked[:20],  # Top 20
            "total_found": len(vector_results)
        }
```

## Initialization Script

```python
# server/scripts/init_vector_db.py
"""Initialize vector database with papers from data/papers"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from app.services.vector_db import VectorDatabase
from app.services.pdf_parser import extract_text_from_pdf

def initialize_from_papers(papers_dir: Path = Path("../../data/papers")):
    print("Initializing vector database...")

    db = VectorDatabase()
    papers = []

    for pdf_path in papers_dir.glob("*.pdf"):
        print(f"Processing {pdf_path.name}...")

        try:
            text = extract_text_from_pdf(pdf_path)

            paper = {
                "id": pdf_path.stem,
                "title": extract_title(text),
                "abstract": extract_abstract(text),
                "full_text": text,
                "source": "local",
                "file_path": str(pdf_path)
            }

            papers.append(paper)

        except Exception as e:
            print(f"Error: {e}")
            continue

    print(f"\nAdding {len(papers)} papers to vector database...")
    db.add_papers(papers)

    print(f"✅ Initialization complete!")
    print(f"Total papers: {db.collection.count()}")

if __name__ == "__main__":
    initialize_from_papers()
```

**Usage:**
```bash
cd server
python scripts/init_vector_db.py
```

## Performance Characteristics

### Query Performance
- **Embedding generation:** ~10ms per query (CPU)
- **Vector search:** ~50-200ms for 10k documents
- **Total query time:** ~100-250ms (acceptable)

### Ingestion Performance
- **Embedding generation:** ~3000 docs/sec (CPU)
- **Database write:** ~1000 docs/sec
- **Initial load (10k papers):** ~10-20 minutes

### Storage Requirements
- **Embeddings:** ~1.5KB per document (384 dim × 4 bytes)
- **10k papers:** ~15MB embeddings + ~50MB SQLite
- **100k papers:** ~150MB embeddings + ~500MB SQLite

## Migration Strategy

### Phase 1: Development (Current)
- ChromaDB with local storage
- Single-machine deployment
- Up to 100k documents
- CPU-based embeddings

### Phase 2: Production (If needed)
```python
# Option 1: Stay with Chroma (add optimizations)
- Add Redis caching layer
- GPU for faster embedding generation
- Batch processing optimizations

# Option 2: Migrate to Weaviate (for scale)
- Docker deployment
- Better clustering support
- GraphQL API
- 1M+ documents

# Option 3: Migrate to Qdrant (for performance)
- High-performance Rust core
- Better filtering
- Distributed deployment
```

## Dependencies

```txt
# requirements.txt
chromadb==0.4.18
sentence-transformers==2.2.2
```

**Installation:**
```bash
pip install chromadb sentence-transformers
```

**First run downloads:**
- sentence-transformers/all-MiniLM-L6-v2 (~80MB)
- ChromaDB dependencies

## Testing

```python
# tests/test_vector_db.py
import pytest
from app.services.vector_db import VectorDatabase

def test_add_and_search(tmp_path):
    db = VectorDatabase(storage_path=str(tmp_path / "test_chroma"))

    # Add test papers
    db.add_papers([
        {
            "id": "paper1",
            "title": "CRISPR gene editing in bioink scaffolds",
            "abstract": "We demonstrate CRISPR editing..."
        }
    ])

    # Search
    results = db.search("CRISPR gene editing", n_results=1)

    assert len(results) == 1
    assert results[0]["id"] == "paper1"
    assert results[0]["similarity"] > 0.7
```

## Monitoring

```python
# Add to VectorDatabase class
def get_stats(self) -> dict:
    return {
        "total_papers": self.collection.count(),
        "embedding_model": "all-MiniLM-L6-v2",
        "embedding_dimension": 384,
        "storage_path": str(self.client._settings.persist_directory)
    }
```

## Decision Summary

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| **Database** | ChromaDB | Easiest setup, Python-native, embedded |
| **Embedding Model** | all-MiniLM-L6-v2 | Fast, free, good quality |
| **Storage** | Local file system | Developer-configurable paths |
| **Dimension** | 384 | Good balance of quality vs storage |
| **Distance Metric** | Cosine | Standard for semantic similarity |

## References

- Comprehensive analysis: specs/VECTOR_DATABASE_SPEC.md
- ChromaDB documentation: https://docs.trychroma.com/
- Sentence Transformers: https://www.sbert.net/
- specs/MULTI_AGENT_ARCHITECTURE.md (Research Agent integration)

## Next Steps

1. ✅ Document decision (this file)
2. Install ChromaDB and sentence-transformers
3. Implement VectorDatabase class
4. Create initialization script
5. Integrate with Research Agent
6. Test with data/papers corpus
7. Update GitHub issue #4
