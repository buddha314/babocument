"""
Tests for Vector Database Service (ChromaDB wrapper).
"""

import pytest
from app.services.vector_db import VectorDatabase


class TestVectorDatabaseInitialization:
    """Test VectorDatabase initialization."""

    def test_init_creates_collection(self, vector_db):
        """Test that initialization creates a collection."""
        assert vector_db.collection is not None
        assert vector_db.collection.name == "research_papers"

    def test_init_with_custom_path(self, temp_db_path):
        """Test initialization with custom storage path."""
        custom_path = temp_db_path / "custom"
        db = VectorDatabase(storage_path=str(custom_path))
        
        assert db.storage_path == custom_path
        assert custom_path.exists()

    def test_initial_stats(self, vector_db):
        """Test database stats on empty database."""
        stats = vector_db.get_stats()
        
        assert stats["total_papers"] == 0
        assert stats["embedding_model"] == "all-MiniLM-L6-v2"
        assert stats["embedding_dimension"] == 384
        assert stats["collection_name"] == "research_papers"


class TestAddPapers:
    """Test adding papers to the database."""

    def test_add_single_paper(self, vector_db, sample_papers):
        """Test adding a single paper."""
        count = vector_db.add_papers([sample_papers[0]])
        
        assert count == 1
        assert vector_db.collection.count() == 1

    def test_add_multiple_papers(self, vector_db, sample_papers):
        """Test adding multiple papers at once."""
        count = vector_db.add_papers(sample_papers)
        
        assert count == 3
        assert vector_db.collection.count() == 3

    def test_add_empty_list(self, vector_db):
        """Test adding empty list returns 0."""
        count = vector_db.add_papers([])
        
        assert count == 0
        assert vector_db.collection.count() == 0

    def test_paper_metadata_extraction(self, vector_db, sample_papers):
        """Test that paper metadata is correctly extracted."""
        vector_db.add_papers([sample_papers[0]])
        
        paper = vector_db.get_paper("paper1")
        assert paper is not None
        
        metadata = paper["metadata"]
        assert metadata["title"] == sample_papers[0]["title"]
        assert metadata["year"] == 2023
        assert metadata["source"] == "test"
        assert metadata["doi"] == "10.1234/test.001"
        assert "Smith, J." in metadata["authors"]


class TestSearch:
    """Test semantic search functionality."""

    def test_search_returns_relevant_results(self, vector_db, sample_papers):
        """Test search returns relevant papers."""
        vector_db.add_papers(sample_papers)
        
        results = vector_db.search("CRISPR gene editing", n_results=5)
        
        assert len(results) > 0
        # First result should be the CRISPR paper
        assert results[0]["id"] == "paper1"
        assert results[0]["similarity"] > 0.5

    def test_search_similarity_scores(self, vector_db, sample_papers):
        """Test that similar papers have higher scores."""
        vector_db.add_papers(sample_papers)
        
        results = vector_db.search("bioink hydrogel printing", n_results=3)
        
        assert len(results) == 3
        # Bioink papers should score higher than manufacturing paper
        bioink_scores = [r["similarity"] for r in results[:2]]
        manufacturing_score = results[2]["similarity"]
        
        assert all(score > manufacturing_score for score in bioink_scores)

    def test_search_limit_results(self, vector_db, sample_papers):
        """Test that n_results limits the number of results."""
        vector_db.add_papers(sample_papers)
        
        results = vector_db.search("bioprinting", n_results=2)
        
        assert len(results) <= 2

    def test_search_with_year_filter(self, vector_db, sample_papers):
        """Test search with year range filtering."""
        vector_db.add_papers(sample_papers)
        
        results = vector_db.search(
            "bioprinting",
            n_results=5,
            filters={"year_min": 2023}
        )
        
        # Should only return papers from 2023 onwards
        for result in results:
            year = result["metadata"].get("year")
            if year:
                assert year >= 2023

    def test_search_empty_database(self, vector_db):
        """Test search on empty database returns empty list."""
        results = vector_db.search("test query", n_results=5)
        
        assert results == []

    def test_search_includes_metadata(self, vector_db, sample_papers):
        """Test that search results include metadata."""
        vector_db.add_papers(sample_papers)
        
        results = vector_db.search("bioprinting", n_results=1)
        
        assert len(results) > 0
        assert "metadata" in results[0]
        assert "title" in results[0]["metadata"]
        assert "similarity" in results[0]
        assert "id" in results[0]


class TestFindSimilar:
    """Test finding similar papers functionality."""

    def test_find_similar_papers(self, vector_db, sample_papers):
        """Test finding papers similar to a given paper."""
        vector_db.add_papers(sample_papers)
        
        similar = vector_db.find_similar("paper1", n_results=5)
        
        assert len(similar) > 0
        # Should not include the source paper itself
        assert all(r["id"] != "paper1" for r in similar)

    def test_find_similar_excludes_self(self, vector_db, sample_papers):
        """Test that find_similar excludes the source paper."""
        vector_db.add_papers(sample_papers)
        
        similar = vector_db.find_similar("paper2", n_results=10)
        
        paper_ids = [r["id"] for r in similar]
        assert "paper2" not in paper_ids

    def test_find_similar_nonexistent_paper(self, vector_db, sample_papers):
        """Test find_similar with non-existent paper ID."""
        vector_db.add_papers(sample_papers)
        
        similar = vector_db.find_similar("nonexistent", n_results=5)
        
        assert similar == []

    def test_find_similar_returns_most_similar(self, vector_db, sample_papers):
        """Test that similar papers have high similarity scores."""
        vector_db.add_papers(sample_papers)
        
        # Paper1 (CRISPR bioprinting) should be similar to Paper2 (bioinks)
        similar = vector_db.find_similar("paper1", n_results=5)
        
        assert len(similar) > 0
        # Most similar should have decent similarity score
        assert similar[0]["similarity"] > 0.3


class TestGetPaper:
    """Test retrieving individual papers."""

    def test_get_existing_paper(self, vector_db, sample_papers):
        """Test retrieving an existing paper."""
        vector_db.add_papers(sample_papers)
        
        paper = vector_db.get_paper("paper1")
        
        assert paper is not None
        assert paper["id"] == "paper1"
        assert "metadata" in paper
        assert "document" in paper

    def test_get_nonexistent_paper(self, vector_db):
        """Test retrieving a non-existent paper returns None."""
        paper = vector_db.get_paper("nonexistent")
        
        assert paper is None


class TestDeletePaper:
    """Test deleting papers."""

    def test_delete_existing_paper(self, vector_db, sample_papers):
        """Test deleting an existing paper."""
        vector_db.add_papers(sample_papers)
        initial_count = vector_db.collection.count()
        
        result = vector_db.delete_paper("paper1")
        
        assert result is True
        assert vector_db.collection.count() == initial_count - 1
        assert vector_db.get_paper("paper1") is None

    def test_delete_and_search(self, vector_db, sample_papers):
        """Test that deleted papers don't appear in search."""
        vector_db.add_papers(sample_papers)
        vector_db.delete_paper("paper1")
        
        results = vector_db.search("CRISPR gene editing", n_results=5)
        
        paper_ids = [r["id"] for r in results]
        assert "paper1" not in paper_ids


class TestReset:
    """Test database reset functionality."""

    def test_reset_clears_database(self, vector_db, sample_papers):
        """Test that reset clears all papers."""
        vector_db.add_papers(sample_papers)
        assert vector_db.collection.count() > 0
        
        vector_db.reset()
        
        assert vector_db.collection.count() == 0

    def test_reset_allows_new_additions(self, vector_db, sample_papers):
        """Test that database can be used after reset."""
        vector_db.add_papers(sample_papers)
        vector_db.reset()
        
        # Should be able to add papers again
        count = vector_db.add_papers([sample_papers[0]])
        assert count == 1
        assert vector_db.collection.count() == 1


class TestPrivateHelpers:
    """Test private helper methods."""

    def test_prepare_text(self, vector_db):
        """Test text preparation for embedding."""
        paper = {
            "title": "Test Title",
            "abstract": "Test abstract with details.",
            "full_text": "Full text " * 1000,  # Long text
        }
        
        text = vector_db._prepare_text(paper)
        
        # Title and abstract should be duplicated (weighted)
        assert text.count("Test Title") == 2
        assert text.count("Test abstract") == 2
        # Full text should be truncated
        assert len(text) < len("Full text " * 1000) + 200

    def test_extract_metadata(self, vector_db):
        """Test metadata extraction."""
        paper = {
            "title": "Test Title",
            "authors": ["Author One", "Author Two"],
            "year": 2024,
            "source": "test_source",
            "doi": "10.1234/test",
        }
        
        metadata = vector_db._extract_metadata(paper)
        
        assert metadata["title"] == "Test Title"
        assert "Author One" in metadata["authors"]
        assert metadata["year"] == 2024
        assert metadata["source"] == "test_source"
        assert metadata["doi"] == "10.1234/test"

    def test_build_filters_year_range(self, vector_db):
        """Test building year range filters."""
        filters = {"year_min": 2020, "year_max": 2023}
        
        where = vector_db._build_filters(filters)
        
        assert where is not None
        assert "year" in where
        assert where["year"]["$gte"] == 2020
        assert where["year"]["$lte"] == 2023

    def test_build_filters_empty(self, vector_db):
        """Test building filters with empty dict."""
        filters = {}
        
        where = vector_db._build_filters(filters)
        
        assert where is None


@pytest.mark.integration
class TestEndToEnd:
    """End-to-end integration tests."""

    def test_full_workflow(self, vector_db, sample_papers):
        """Test complete workflow: add, search, find similar, delete."""
        # Add papers
        count = vector_db.add_papers(sample_papers)
        assert count == 3
        
        # Search
        results = vector_db.search("bioprinting CRISPR", n_results=5)
        assert len(results) > 0
        top_paper_id = results[0]["id"]
        
        # Find similar
        similar = vector_db.find_similar(top_paper_id, n_results=5)
        assert len(similar) > 0
        
        # Get specific paper
        paper = vector_db.get_paper(top_paper_id)
        assert paper is not None
        
        # Delete
        vector_db.delete_paper(top_paper_id)
        assert vector_db.get_paper(top_paper_id) is None
        
        # Verify stats
        stats = vector_db.get_stats()
        assert stats["total_papers"] == 2

    def test_multiple_search_queries(self, vector_db, sample_papers):
        """Test multiple consecutive searches."""
        vector_db.add_papers(sample_papers)
        
        queries = [
            "CRISPR gene editing",
            "hydrogel bioink",
            "neural network manufacturing",
            "3D printing tissue engineering",
        ]
        
        for query in queries:
            results = vector_db.search(query, n_results=3)
            assert len(results) <= 3
            # All results should have similarity scores
            for result in results:
                assert 0 <= result["similarity"] <= 1
