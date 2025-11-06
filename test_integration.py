"""
Quick integration test for API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoint(method, path, data=None, description=""):
    print(f"\n{'='*60}")
    print(f"Testing: {method} {path}")
    if description:
        print(f"Description: {description}")
    print('='*60)
    
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{path}", timeout=5)
        elif method == "POST":
            response = requests.post(f"{BASE_URL}{path}", json=data, timeout=5)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code < 400:
            try:
                result = response.json()
                print(f"Response: {json.dumps(result, indent=2)[:500]}")
            except:
                print(f"Response: {response.text[:200]}")
        else:
            print(f"Error: {response.text[:200]}")
            
        return response.status_code < 400
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

print("="*60)
print("API Integration Tests")
print("="*60)

# Test basic endpoints
test_endpoint("GET", "/", description="Root endpoint")
test_endpoint("GET", "/health", description="Health check")
test_endpoint("GET", "/api/v1/stats", description="System stats")
test_endpoint("GET", "/api/v1/stats/all", description="All stats")

# Test document endpoints
test_endpoint("GET", "/api/v1/documents", description="List all documents")
test_endpoint("GET", "/api/v1/documents?limit=5", description="List with pagination")

# Test repository endpoints  
test_endpoint("GET", "/api/v1/repositories", description="List repositories")
test_endpoint("GET", "/api/v1/repositories/local/status", description="Local repo status")
test_endpoint("POST", "/api/v1/repositories/local/test", description="Test local connection")

# Test search
search_query = {
    "query": "bioink",
    "limit": 5,
    "search_type": "semantic"
}
test_endpoint("POST", "/api/v1/documents/search", data=search_query, description="Search documents")

print("\n" + "="*60)
print("Tests completed!")
print("="*60)
