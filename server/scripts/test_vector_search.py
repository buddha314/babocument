"""
Test Vector Database Search

Quick test script to verify semantic search functionality.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.vector_db import get_vector_db


def main():
    print("\n" + "="*60)
    print("Vector Database Search Test")
    print("="*60 + "\n")
    
    # Get database instance
    db = get_vector_db()
    
    # Show stats
    stats = db.get_stats()
    print(f"Database loaded: {stats['total_papers']} papers")
    print(f"Embedding model: {stats['embedding_model']}\n")
    print("="*60 + "\n")
    
    # Test queries
    test_queries = [
        "3D bioprinting techniques",
        "bioink materials and properties",
        "scaffold design for tissue engineering",
        "CRISPR gene editing",  # Should return low similarity
    ]
    
    for query in test_queries:
        print(f"Query: '{query}'")
        print("-" * 60)
        
        results = db.search(query, n_results=3)
        
        if not results:
            print("  No results found.\n")
            continue
        
        for i, result in enumerate(results, 1):
            similarity = result['similarity']
            title = result['metadata'].get('title', 'Untitled')
            
            # Truncate title if too long
            if len(title) > 60:
                title = title[:57] + "..."
            
            print(f"  {i}. [{similarity:.3f}] {title}")
        
        print()
    
    print("="*60)
    print("✅ Search test complete!")
    print("="*60)


if __name__ == "__main__":
    main()
