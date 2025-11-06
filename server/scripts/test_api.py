"""
Test script for REST API endpoints

Quick validation that all endpoints are accessible and return expected responses.
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"


def test_endpoint(method: str, path: str, **kwargs):
    """Test an API endpoint"""
    url = f"{BASE_URL}{path}"
    print(f"\n{'='*60}")
    print(f"Testing: {method} {path}")
    print(f"{'='*60}")
    
    try:
        if method == "GET":
            response = requests.get(url, **kwargs)
        elif method == "POST":
            response = requests.post(url, **kwargs)
        else:
            print(f"Unsupported method: {method}")
            return
        
        print(f"Status: {response.status_code}")
        print(f"Response:")
        print(json.dumps(response.json(), indent=2))
        
        return response
    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    """Run all endpoint tests"""
    print("\n" + "="*60)
    print("REST API Endpoint Tests")
    print("="*60)
    
    # Root and health
    test_endpoint("GET", "/")
    test_endpoint("GET", "/health")
    
    # Documents
    test_endpoint("GET", "/api/v1/documents")
    test_endpoint("GET", "/api/v1/documents?limit=5&offset=0")
    test_endpoint("GET", "/api/v1/documents/test-id-123")
    test_endpoint("POST", "/api/v1/documents/search", 
                  json={"query": "bioinks", "limit": 10, "search_type": "semantic"})
    
    # Repositories
    test_endpoint("GET", "/api/v1/repositories")
    test_endpoint("GET", "/api/v1/repositories/pubmed/status")
    test_endpoint("POST", "/api/v1/repositories/sync",
                  json={"repository_id": "pubmed", "full_sync": False})
    test_endpoint("GET", "/api/v1/repositories/local/documents?limit=10")
    
    # Stats
    test_endpoint("GET", "/api/v1/stats")
    test_endpoint("GET", "/api/v1/stats/all")
    test_endpoint("GET", "/api/v1/status/processing")
    test_endpoint("GET", "/api/v1/stats/agents")
    
    print("\n" + "="*60)
    print("All tests completed!")
    print("="*60)


if __name__ == "__main__":
    main()
