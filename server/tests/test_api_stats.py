"""
Test suite for Statistics and Status API endpoints

Tests all system statistics and processing status endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime

from app.main import app


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


class TestSystemStats:
    """Tests for GET /api/v1/stats"""
    
    def test_get_system_stats(self, client):
        """Test getting system statistics"""
        response = client.get("/api/v1/stats")
        assert response.status_code == 200
        
        data = response.json()
        assert "total_documents" in data
        assert "indexed_documents" in data
        assert "repositories_count" in data
        assert "total_embeddings" in data
        assert "storage_used_mb" in data
        assert "last_updated" in data
        assert "uptime_seconds" in data
    
    def test_stats_data_types(self, client):
        """Test that stats have correct data types"""
        response = client.get("/api/v1/stats")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data["total_documents"], int)
        assert isinstance(data["indexed_documents"], int)
        assert isinstance(data["repositories_count"], int)
        assert isinstance(data["total_embeddings"], int)
        assert isinstance(data["storage_used_mb"], (int, float))
        assert isinstance(data["uptime_seconds"], (int, float))
        
        # Validate timestamp
        datetime.fromisoformat(data["last_updated"])
    
    def test_stats_non_negative_values(self, client):
        """Test that all counts are non-negative"""
        response = client.get("/api/v1/stats")
        data = response.json()
        
        assert data["total_documents"] >= 0
        assert data["indexed_documents"] >= 0
        assert data["repositories_count"] >= 0
        assert data["total_embeddings"] >= 0
        assert data["storage_used_mb"] >= 0
        assert data["uptime_seconds"] >= 0


class TestAllStats:
    """Tests for GET /api/v1/stats/all"""
    
    def test_get_all_stats(self, client):
        """Test getting comprehensive statistics"""
        response = client.get("/api/v1/stats/all")
        assert response.status_code == 200
        
        data = response.json()
        assert "system" in data
        assert "repositories" in data
        assert "documents" in data
        assert "agents" in data
    
    def test_all_stats_structure(self, client):
        """Test comprehensive stats structure"""
        response = client.get("/api/v1/stats/all")
        data = response.json()
        
        # System stats
        assert "total_documents" in data["system"]
        
        # Repositories stats
        assert isinstance(data["repositories"], list)
        
        # Documents stats
        assert "by_year" in data["documents"]
        assert "by_source" in data["documents"]
        assert "by_type" in data["documents"]
        assert "top_authors" in data["documents"]
        assert "top_journals" in data["documents"]
        
        # Agents stats
        assert isinstance(data["agents"], list)


class TestProcessingStatus:
    """Tests for GET /api/v1/status/processing"""
    
    def test_get_processing_status_default(self, client):
        """Test getting processing status with defaults"""
        response = client.get("/api/v1/status/processing")
        assert response.status_code == 200
        
        data = response.json()
        assert "pending_tasks" in data
        assert "running_tasks" in data
        assert "completed_tasks" in data
        assert "failed_tasks" in data
        assert "tasks" in data
    
    def test_get_processing_status_with_limit(self, client):
        """Test processing status with custom limit"""
        response = client.get("/api/v1/status/processing?limit=10")
        assert response.status_code == 200
    
    def test_get_processing_status_filter_by_status(self, client):
        """Test filtering processing tasks by status"""
        statuses = ["pending", "running", "completed", "failed"]
        
        for status in statuses:
            response = client.get(f"/api/v1/status/processing?status={status}")
            assert response.status_code == 200
    
    def test_processing_status_counts(self, client):
        """Test that task counts are integers"""
        response = client.get("/api/v1/status/processing")
        data = response.json()
        
        assert isinstance(data["pending_tasks"], int)
        assert isinstance(data["running_tasks"], int)
        assert isinstance(data["completed_tasks"], int)
        assert isinstance(data["failed_tasks"], int)
        assert data["pending_tasks"] >= 0
        assert data["running_tasks"] >= 0
        assert data["completed_tasks"] >= 0
        assert data["failed_tasks"] >= 0
    
    def test_processing_tasks_list(self, client):
        """Test tasks list structure"""
        response = client.get("/api/v1/status/processing")
        data = response.json()
        
        assert isinstance(data["tasks"], list)


class TestTaskStatus:
    """Tests for GET /api/v1/status/processing/{task_id}"""
    
    def test_get_task_status_not_found(self, client):
        """Test getting non-existent task"""
        response = client.get("/api/v1/status/processing/nonexistent-task-id")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_get_task_status_structure(self, client):
        """Test task status response structure"""
        # TODO: Create task first, then query it
        response = client.get("/api/v1/status/processing/test-task-123")
        
        if response.status_code == 200:
            data = response.json()
            assert "task_id" in data
            assert "type" in data
            assert "status" in data
            assert "progress" in data
            assert "created_at" in data
            assert "metadata" in data
            
            # Validate progress is percentage
            assert 0 <= data["progress"] <= 100


class TestAgentStats:
    """Tests for GET /api/v1/stats/agents"""
    
    def test_get_agent_stats(self, client):
        """Test getting agent statistics"""
        response = client.get("/api/v1/stats/agents")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
    
    def test_agent_stats_structure(self, client):
        """Test agent stats structure when agents exist"""
        response = client.get("/api/v1/stats/agents")
        data = response.json()
        
        # If agents exist, validate structure
        if len(data) > 0:
            agent = data[0]
            assert "agent_name" in agent
            assert "agent_type" in agent
            assert "total_tasks" in agent
            assert "successful_tasks" in agent
            assert "failed_tasks" in agent
            assert "avg_execution_time_ms" in agent
            
            # Validate data types
            assert isinstance(agent["total_tasks"], int)
            assert isinstance(agent["successful_tasks"], int)
            assert isinstance(agent["failed_tasks"], int)
            assert isinstance(agent["avg_execution_time_ms"], (int, float))
            
            # Validate non-negative values
            assert agent["total_tasks"] >= 0
            assert agent["successful_tasks"] >= 0
            assert agent["failed_tasks"] >= 0
            assert agent["avg_execution_time_ms"] >= 0
    
    def test_agent_stats_consistency(self, client):
        """Test agent stats logical consistency"""
        response = client.get("/api/v1/stats/agents")
        data = response.json()
        
        for agent in data:
            # Total tasks should equal successful + failed
            assert agent["total_tasks"] >= agent["successful_tasks"]
            assert agent["total_tasks"] >= agent["failed_tasks"]


class TestHealthCheck:
    """Tests for basic health endpoints"""
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "status" in data
        assert "environment" in data
        assert data["status"] == "running"
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "environment" in data
        assert data["status"] == "healthy"


class TestErrorHandling:
    """Tests for error handling across all endpoints"""
    
    def test_invalid_json_body(self, client):
        """Test handling of invalid JSON in request body"""
        response = client.post(
            "/api/v1/documents/search",
            data="invalid json{{{",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_missing_required_fields(self, client):
        """Test validation of required fields"""
        # Search without query field
        response = client.post("/api/v1/documents/search", json={})
        assert response.status_code == 422
    
    def test_invalid_route(self, client):
        """Test 404 for invalid routes"""
        response = client.get("/api/v1/nonexistent/endpoint")
        assert response.status_code == 404
