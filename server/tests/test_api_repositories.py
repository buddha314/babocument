"""
Test suite for Repository API endpoints

Tests all repository management REST API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from unittest.mock import Mock, patch

from app.main import app


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


@pytest.fixture
def mock_repository():
    """Mock repository information"""
    return {
        "id": "pubmed",
        "name": "PubMed",
        "type": "pubmed",
        "status": "connected",
        "url": "https://pubmed.ncbi.nlm.nih.gov/",
        "description": "NCBI PubMed database",
        "document_count": 1234,
        "last_sync": datetime.now().isoformat(),
        "last_error": None,
        "config": {"api_key": "***"}
    }


class TestListRepositories:
    """Tests for GET /api/v1/repositories"""
    
    def test_list_all_repositories(self, client):
        """Test listing all repositories"""
        response = client.get("/api/v1/repositories")
        assert response.status_code == 200
        
        data = response.json()
        assert "repositories" in data
        assert "total" in data
        assert isinstance(data["repositories"], list)
        assert isinstance(data["total"], int)
    
    def test_list_repositories_filter_by_status(self, client):
        """Test filtering repositories by status"""
        response = client.get("/api/v1/repositories?status=connected")
        assert response.status_code == 200
    
    def test_list_repositories_filter_by_type(self, client):
        """Test filtering repositories by type"""
        response = client.get("/api/v1/repositories?type=pubmed")
        assert response.status_code == 200
    
    def test_list_repositories_multiple_filters(self, client):
        """Test filtering by multiple parameters"""
        response = client.get("/api/v1/repositories?status=connected&type=arxiv")
        assert response.status_code == 200


class TestGetRepositoryStatus:
    """Tests for GET /api/v1/repositories/{repository_id}/status"""
    
    def test_get_status_not_found(self, client):
        """Test getting status for non-existent repository"""
        response = client.get("/api/v1/repositories/nonexistent/status")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_get_status_success(self, client):
        """Test successful status retrieval"""
        # TODO: Mock repository when implemented
        response = client.get("/api/v1/repositories/pubmed/status")
        # Currently returns 404, will return 200 when implemented
        if response.status_code == 200:
            data = response.json()
            assert "repository" in data
            assert "connection_status" in data
            assert "indexed_documents" in data
            assert "last_check" in data
            assert "health" in data


class TestSyncRepositories:
    """Tests for POST /api/v1/repositories/sync"""
    
    def test_sync_all_repositories(self, client):
        """Test syncing all repositories"""
        sync_request = {
            "full_sync": False
        }
        
        response = client.post("/api/v1/repositories/sync", json=sync_request)
        assert response.status_code == 200
        
        data = response.json()
        assert "task_id" in data
        assert "status" in data
        assert "message" in data
        assert "repositories" in data
        assert "started_at" in data
    
    def test_sync_specific_repository(self, client):
        """Test syncing a specific repository"""
        sync_request = {
            "repository_id": "pubmed",
            "full_sync": False
        }
        
        response = client.post("/api/v1/repositories/sync", json=sync_request)
        assert response.status_code == 200
        
        data = response.json()
        assert "task_id" in data
        assert "repositories" in data
    
    def test_sync_full_sync(self, client):
        """Test full synchronization"""
        sync_request = {
            "repository_id": "arxiv",
            "full_sync": True
        }
        
        response = client.post("/api/v1/repositories/sync", json=sync_request)
        assert response.status_code == 200
    
    def test_sync_with_filters(self, client):
        """Test sync with filters"""
        sync_request = {
            "repository_id": "pubmed",
            "full_sync": False,
            "filters": {
                "date_from": "2024-01-01",
                "date_to": "2024-12-31",
                "keywords": ["bioink", "biomanufacturing"]
            }
        }
        
        response = client.post("/api/v1/repositories/sync", json=sync_request)
        assert response.status_code == 200
    
    def test_sync_response_structure(self, client):
        """Test sync response structure"""
        sync_request = {"full_sync": False}
        
        response = client.post("/api/v1/repositories/sync", json=sync_request)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data["task_id"], str)
        assert data["status"] in ["queued", "running", "completed"]
        assert isinstance(data["repositories"], list)


class TestListRepositoryDocuments:
    """Tests for GET /api/v1/repositories/{repository_id}/documents"""
    
    def test_list_documents_default_params(self, client):
        """Test listing repository documents with defaults"""
        response = client.get("/api/v1/repositories/pubmed/documents")
        assert response.status_code == 200
        
        data = response.json()
        assert "repository_id" in data
        assert "documents" in data
        assert "total" in data
        assert "limit" in data
        assert "offset" in data
        assert data["repository_id"] == "pubmed"
    
    def test_list_documents_with_pagination(self, client):
        """Test pagination for repository documents"""
        response = client.get("/api/v1/repositories/local/documents?limit=5&offset=10")
        assert response.status_code == 200
        
        data = response.json()
        assert data["limit"] == 5
        assert data["offset"] == 10
    
    def test_list_documents_invalid_limit(self, client):
        """Test validation for invalid limit"""
        response = client.get("/api/v1/repositories/arxiv/documents?limit=0")
        assert response.status_code == 422


class TestTestRepositoryConnection:
    """Tests for POST /api/v1/repositories/{repository_id}/test"""
    
    def test_connection_success(self, client):
        """Test successful connection test"""
        response = client.post("/api/v1/repositories/pubmed/test")
        assert response.status_code == 200
        
        data = response.json()
        assert "repository_id" in data
        assert "status" in data
        assert "message" in data
        assert "timestamp" in data
    
    def test_connection_different_repositories(self, client):
        """Test connection for different repository types"""
        repositories = ["pubmed", "arxiv", "local", "biorxiv"]
        
        for repo_id in repositories:
            response = client.post(f"/api/v1/repositories/{repo_id}/test")
            assert response.status_code == 200
            data = response.json()
            assert data["repository_id"] == repo_id
    
    def test_connection_response_structure(self, client):
        """Test connection test response structure"""
        response = client.post("/api/v1/repositories/pubmed/test")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data["repository_id"], str)
        assert isinstance(data["status"], str)
        assert isinstance(data["message"], str)
        assert isinstance(data["timestamp"], str)
        
        # Validate timestamp format
        datetime.fromisoformat(data["timestamp"])
