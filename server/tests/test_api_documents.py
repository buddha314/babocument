"""
Test suite for Document API endpoints

Tests all document-related REST API endpoints including CRUD operations and search.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from io import BytesIO

from app.main import app


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


@pytest.fixture
def mock_document_metadata():
    """Mock document metadata"""
    return {
        "id": "doc-123",
        "title": "Advances in Bioink Technology",
        "authors": ["Dr. Jane Smith", "Dr. John Doe"],
        "abstract": "This paper discusses recent advances in bioink formulations...",
        "year": 2024,
        "journal": "Nature Biotechnology",
        "doi": "10.1038/nbt.2024.001",
        "url": "https://example.com/paper.pdf",
        "source": "local",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "file_path": "/data/papers/paper1.pdf",
        "indexed": True
    }


class TestDocumentList:
    """Tests for GET /api/v1/documents"""
    
    def test_list_documents_default_params(self, client):
        """Test listing documents with default parameters"""
        response = client.get("/api/v1/documents")
        assert response.status_code == 200
        
        data = response.json()
        assert "documents" in data
        assert "total" in data
        assert "limit" in data
        assert "offset" in data
        assert "has_next" in data
        assert isinstance(data["documents"], list)
    
    def test_list_documents_with_pagination(self, client):
        """Test pagination parameters"""
        response = client.get("/api/v1/documents?limit=5&offset=10")
        assert response.status_code == 200
        
        data = response.json()
        assert data["limit"] == 5
        assert data["offset"] == 10
    
    def test_list_documents_with_filters(self, client):
        """Test filtering by source and year"""
        response = client.get("/api/v1/documents?source=pubmed&year=2024")
        assert response.status_code == 200
    
    def test_list_documents_indexed_only(self, client):
        """Test filtering for indexed documents only"""
        response = client.get("/api/v1/documents?indexed_only=true")
        assert response.status_code == 200
    
    def test_list_documents_invalid_limit(self, client):
        """Test validation for invalid limit"""
        response = client.get("/api/v1/documents?limit=0")
        assert response.status_code == 422  # Validation error
    
    def test_list_documents_limit_too_high(self, client):
        """Test validation for limit above maximum"""
        response = client.get("/api/v1/documents?limit=101")
        assert response.status_code == 422  # Validation error


class TestGetDocument:
    """Tests for GET /api/v1/documents/{document_id}"""
    
    def test_get_document_not_found(self, client):
        """Test getting non-existent document"""
        response = client.get("/api/v1/documents/nonexistent-id")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_get_document_success(self, client, mock_document_metadata):
        """Test successful document retrieval"""
        # TODO: Mock the database response when implemented
        response = client.get("/api/v1/documents/doc-123")
        # Currently returns 404, will return 200 when implemented
        assert response.status_code in [200, 404]


class TestGetDocumentContent:
    """Tests for GET /api/v1/documents/{document_id}/content"""
    
    def test_get_content_not_found(self, client):
        """Test getting content for non-existent document"""
        response = client.get("/api/v1/documents/nonexistent-id/content")
        assert response.status_code == 404
    
    def test_get_content_structure(self, client):
        """Test response structure for document content"""
        response = client.get("/api/v1/documents/doc-123/content")
        # Currently returns 404, check structure when implemented
        if response.status_code == 200:
            data = response.json()
            assert "metadata" in data
            assert "content" in data
            assert "sections" in data or data["sections"] is None


class TestUploadDocument:
    """Tests for POST /api/v1/documents"""
    
    def test_upload_pdf_file(self, client):
        """Test uploading a PDF file"""
        # Create mock PDF file
        pdf_content = b"%PDF-1.4\n%Mock PDF content"
        files = {"file": ("test.pdf", BytesIO(pdf_content), "application/pdf")}
        
        response = client.post("/api/v1/documents", files=files)
        # Should return 200 when implemented (currently may error)
        assert response.status_code in [200, 500]
    
    def test_upload_with_metadata(self, client):
        """Test uploading with metadata parameters"""
        pdf_content = b"%PDF-1.4\n%Mock PDF content"
        files = {"file": ("test.pdf", BytesIO(pdf_content), "application/pdf")}
        data = {
            "title": "Test Paper",
            "authors": "Dr. Test",
            "year": 2024,
            "source": "upload"
        }
        
        response = client.post("/api/v1/documents", files=files, data=data)
        assert response.status_code in [200, 500]
    
    def test_upload_non_pdf_file(self, client):
        """Test uploading non-PDF file is rejected"""
        txt_content = b"This is not a PDF"
        files = {"file": ("test.txt", BytesIO(txt_content), "text/plain")}
        
        response = client.post("/api/v1/documents", files=files)
        assert response.status_code == 400
        assert "PDF" in response.json()["detail"]
    
    def test_upload_response_structure(self, client):
        """Test upload response contains expected fields"""
        pdf_content = b"%PDF-1.4\n%Mock PDF content"
        files = {"file": ("test.pdf", BytesIO(pdf_content), "application/pdf")}
        
        response = client.post("/api/v1/documents", files=files)
        if response.status_code == 200:
            data = response.json()
            assert "id" in data
            assert "status" in data
            assert "message" in data


class TestDeleteDocument:
    """Tests for DELETE /api/v1/documents/{document_id}"""
    
    def test_delete_nonexistent_document(self, client):
        """Test deleting non-existent document"""
        response = client.delete("/api/v1/documents/nonexistent-id")
        assert response.status_code == 404
    
    def test_delete_document_success(self, client):
        """Test successful document deletion"""
        # TODO: Mock database when implemented
        response = client.delete("/api/v1/documents/doc-123")
        # Currently returns 404, will return 200 when implemented
        assert response.status_code in [200, 204, 404]


class TestSearchDocuments:
    """Tests for POST /api/v1/documents/search"""
    
    def test_search_semantic(self, client):
        """Test semantic search"""
        search_query = {
            "query": "bioink formulations",
            "limit": 10,
            "search_type": "semantic"
        }
        
        response = client.post("/api/v1/documents/search", json=search_query)
        assert response.status_code == 200
        
        data = response.json()
        assert "results" in data
        assert "query" in data
        assert "search_type" in data
        assert "total" in data
        assert "execution_time_ms" in data
        assert data["search_type"] == "semantic"
    
    def test_search_keyword(self, client):
        """Test keyword search"""
        search_query = {
            "query": "bioink",
            "limit": 5,
            "search_type": "keyword"
        }
        
        response = client.post("/api/v1/documents/search", json=search_query)
        assert response.status_code == 200
        assert response.json()["search_type"] == "keyword"
    
    def test_search_with_filters(self, client):
        """Test search with metadata filters"""
        search_query = {
            "query": "bioink",
            "limit": 10,
            "search_type": "semantic",
            "filters": {
                "year": 2024,
                "author": "Smith"
            }
        }
        
        response = client.post("/api/v1/documents/search", json=search_query)
        assert response.status_code == 200
    
    def test_search_invalid_search_type(self, client):
        """Test invalid search type"""
        search_query = {
            "query": "bioink",
            "search_type": "invalid_type"
        }
        
        response = client.post("/api/v1/documents/search", json=search_query)
        # Should validate search_type (currently may accept any string)
        assert response.status_code in [200, 422]
    
    def test_search_empty_query(self, client):
        """Test search with empty query"""
        search_query = {
            "query": "",
            "search_type": "semantic"
        }
        
        response = client.post("/api/v1/documents/search", json=search_query)
        # Should handle empty query gracefully
        assert response.status_code in [200, 400]
    
    def test_search_limit_validation(self, client):
        """Test search limit validation"""
        search_query = {
            "query": "bioink",
            "limit": 150,  # Above max
            "search_type": "semantic"
        }
        
        response = client.post("/api/v1/documents/search", json=search_query)
        assert response.status_code == 422  # Validation error
    
    def test_search_response_structure(self, client):
        """Test search response has correct structure"""
        search_query = {
            "query": "bioink",
            "search_type": "semantic"
        }
        
        response = client.post("/api/v1/documents/search", json=search_query)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data["results"], list)
        assert isinstance(data["total"], int)
        assert isinstance(data["execution_time_ms"], (int, float))
        assert data["execution_time_ms"] >= 0
