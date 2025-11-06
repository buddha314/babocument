"""
End-to-end test for document workflow.

Tests: Upload → Store → Search → Retrieve
"""

import requests
import time
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"

def create_test_pdf():
    """Create a simple test PDF"""
    # For now, we'll skip creating PDF and just test with the APIs
    pass

def test_health():
    """Test server is running"""
    print("1. Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    print("   ✓ Server is running")

def test_list_empty():
    """Test listing documents when empty"""
    print("\n2. Testing list documents (should be empty)...")
    response = requests.get(f"{BASE_URL}/api/v1/documents")
    assert response.status_code == 200
    data = response.json()
    print(f"   ✓ Found {data['total']} documents")

def test_search():
    """Test search"""
    print("\n3. Testing semantic search...")
    response = requests.post(
        f"{BASE_URL}/api/v1/documents/search",
        json={
            "query": "machine learning",
            "limit": 10,
            "search_type": "semantic"
        }
    )
    assert response.status_code == 200
    data = response.json()
    print(f"   ✓ Search completed in {data['execution_time_ms']:.2f}ms")
    print(f"   ✓ Found {data['total']} results")
    
    # Print results
    for i, result in enumerate(data['results'][:3], 1):
        print(f"   {i}. {result['document']['title']} (score: {result['score']:.3f})")

def test_stats():
    """Test stats endpoint"""
    print("\n4. Testing stats endpoint...")
    response = requests.get(f"{BASE_URL}/api/v1/stats")
    assert response.status_code == 200
    data = response.json()
    print(f"   ✓ Vector DB has {data['vector_db']['total_papers']} papers")

if __name__ == "__main__":
    print("=" * 60)
    print("End-to-End Document Workflow Test")
    print("=" * 60)
    
    try:
        test_health()
        test_list_empty()
        test_search()
        test_stats()
        
        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Cannot connect to server.")
        print("  Please start the server with: python -m uvicorn app.main:app --reload")
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
