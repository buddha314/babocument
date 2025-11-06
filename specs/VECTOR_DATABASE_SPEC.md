# Vector Database Specification

**Created:** 2025-11-06
**Purpose:** Define vector database selection, configuration, and usage for semantic search

## Overview

Babocument requires a vector database to enable semantic search across research papers, find similar documents, and power AI-driven recommendations. The vector database will store document embeddings generated from full-text papers and enable efficient similarity search.

## Requirements

### Functional Requirements

1. **Semantic Search**
   - Find papers by meaning, not just keywords
   - Handle paraphrased queries
   - Understand scientific terminology

2. **Similarity Search**
   - Find papers similar to a given paper
   - Cluster related research
   - Discover connections across topics

3. **Hybrid Search**
   - Combine vector similarity with keyword search
   - Filter by metadata (year, author, journal)
   - Boost recent or highly-cited papers

4. **Scalability**
   - Handle 100,000+ documents initially
   - Scale to 1M+ documents over time
   - Fast query response (< 500ms)

5. **Local Development**
   - Run entirely on local machine
   - No cloud dependencies required
   - Configurable storage paths per developer

### Non-Functional Requirements

1. **Performance**
   - Sub-second similarity search
   - Efficient batch ingestion
   - Support for updates without full reindex

2. **Developer Experience**
   - Easy local setup
   - Simple API
   - Good documentation

3. **Cost**
   - Open source or free tier sufficient
   - Minimal operational overhead
   - No per-query costs

## Vector Database Options

### Option 1: Chroma (Recommended)

**Description:** Lightweight, Python-native vector database designed for AI applications

**Pros:**
- Extremely easy to set up (`pip install chromadb`)
- Runs embedded (no separate server needed)
- Excellent Python integration
- Built-in embedding support (OpenAI, sentence-transformers)
- Persistent local storage
- Active development and community
- Perfect for local development

**Cons:**
- Less mature than enterprise options
- Limited clustering/high availability features
- Smaller ecosystem

**Storage:**
```python
# Local storage path (configurable)
client = chromadb.PersistentClient(path="/path/to/data/chroma")
```

**Use Case Fit:** Excellent for Babocument's needs
- ✅ Easy local development
- ✅ Python-first (matches FastAgent backend)
- ✅ Simple API
- ✅ No separate server process

**Verdict:** **RECOMMENDED** for Phase 1

### Option 2: Weaviate

**Description:** Open-source vector database with rich features

**Pros:**
- Mature and battle-tested
- Rich query capabilities
- Good documentation
- GraphQL API
- Strong consistency

**Cons:**
- Requires Docker container
- More complex setup
- Heavier resource usage
- Steeper learning curve

**Storage:**
```yaml
# Docker volume
volumes:
  - /path/to/data/weaviate:/var/lib/weaviate
```

**Use Case Fit:** Good but overkill for initial needs

**Verdict:** Consider for production scaling

### Option 3: Qdrant

**Description:** High-performance vector similarity search engine

**Pros:**
- Excellent performance
- Rich filtering capabilities
- Good API design
- Active development
- Docker and native options

**Cons:**
- Requires Rust installation for native
- More complex than Chroma
- Smaller Python ecosystem

**Storage:**
```python
# Can run embedded or as server
from qdrant_client import QdrantClient
client = QdrantClient(path="/path/to/data/qdrant")
```

**Use Case Fit:** Strong option, more complex than needed

**Verdict:** Alternative to Chroma

### Option 4: Pinecone

**Description:** Fully managed vector database (cloud service)

**Pros:**
- No infrastructure management
- Excellent performance
- Great documentation
- Generous free tier

**Cons:**
- Cloud-only (not local)
- Not suitable for local development
- Vendor lock-in
- Data privacy concerns

**Verdict:** ❌ Not suitable (requirement: local-first)

### Option 5: Milvus

**Description:** Open-source vector database designed for production scale

**Pros:**
- Production-grade
- Excellent scalability
- Rich features
- Strong consistency

**Cons:**
- Complex deployment (requires Kubernetes or Docker Compose)
- Overkill for initial needs
- Steep learning curve
- Heavy resource requirements

**Verdict:** ❌ Too complex for current needs

### Comparison Matrix

| Feature | Chroma | Weaviate | Qdrant | Pinecone | Milvus |
|---------|--------|----------|--------|----------|--------|
| **Easy Setup** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐ |
| **Local-First** | ✅ | ✅ | ✅ | ❌ | ⚠️ |
| **Python API** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Performance** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Scalability** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Cost** | Free | Free | Free | Free tier | Free |
| **Maturity** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## Recommended Solution: Chroma

**Decision:** Use **ChromaDB** for Phase 1 and early development

**Rationale:**
1. Simplest setup for local development
2. Python-native (perfect for FastAgent)
3. No separate server process needed
4. Configurable storage paths
5. Built-in embedding support
6. Easy to migrate later if needed

**Migration Path:**
- Start with Chroma for MVP
- Monitor performance and scale
- Migrate to Weaviate/Qdrant if needed (>100k docs or production scale)

## Configuration Design

### Directory Structure

```
babocument/
├── server/
│   ├── config/
│   │   └── vector_db_config.yaml
│   └── data/
│       └── chroma/           # Vector DB storage (gitignored)
│           ├── chroma.sqlite3
│           └── embeddings/
├── data/
│   └── papers/              # Source PDFs
│       ├── paper1.pdf
│       └── paper2.pdf
└── .env
```

### Configuration File

**`server/config/vector_db_config.yaml`:**
```yaml
vector_database:
  provider: "chroma"  # or "weaviate", "qdrant"

  chroma:
    storage_path: "${DATA_DIR}/chroma"  # Configurable via env
    collection_name: "research_papers"
    distance_metric: "cosine"  # or "l2", "ip"

  embedding:
    provider: "sentence-transformers"  # or "openai"
    model: "all-MiniLM-L6-v2"  # Fast, good quality
    # model: "all-mpnet-base-v2"  # Better quality, slower
    dimension: 384  # Depends on model

  search:
    default_n_results: 10
    min_similarity_score: 0.7
```

**`.env` (local developer overrides):**
```bash
# Vector Database Configuration
DATA_DIR=/Users/developer/babocument_data
VECTOR_DB_PROVIDER=chroma

# Embedding Configuration
EMBEDDING_PROVIDER=sentence-transformers
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Optional: OpenAI for better embeddings
# OPENAI_API_KEY=sk-...
# EMBEDDING_PROVIDER=openai
# EMBEDDING_MODEL=text-embedding-3-small
```

### Python Configuration Loader

```python
import os
from pathlib import Path
import yaml
from pydantic import BaseSettings

class VectorDBConfig(BaseSettings):
    provider: str = "chroma"
    storage_path: Path
    collection_name: str = "research_papers"
    embedding_model: str = "all-MiniLM-L6-v2"
    dimension: int = 384

    class Config:
        env_prefix = "VECTOR_DB_"

def load_config() -> VectorDBConfig:
    # Load from YAML
    config_path = Path(__file__).parent / "config" / "vector_db_config.yaml"
    with open(config_path) as f:
        yaml_config = yaml.safe_load(f)

    # Override with environment variables
    data_dir = os.getenv("DATA_DIR", "./data")
    storage_path = Path(data_dir) / "chroma"

    return VectorDBConfig(
        storage_path=storage_path,
        **yaml_config.get("vector_database", {}).get("chroma", {})
    )
```

## Embedding Strategy

### Embedding Model Selection

**Option 1: Sentence Transformers (Recommended)**
- **Model:** `all-MiniLM-L6-v2`
- **Dimension:** 384
- **Speed:** Very fast
- **Quality:** Good for general text
- **Cost:** Free (local inference)

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(texts)
```

**Option 2: OpenAI Embeddings**
- **Model:** `text-embedding-3-small`
- **Dimension:** 1536
- **Quality:** Excellent
- **Cost:** $0.02 per 1M tokens (~$0.20 per 10k papers)

```python
from openai import OpenAI

client = OpenAI()
response = client.embeddings.create(
    input=text,
    model="text-embedding-3-small"
)
embedding = response.data[0].embedding
```

**Option 3: Scientific Models**
- **Model:** `allenai/specter2` (paper embeddings)
- **Specialized for scientific papers**
- **Better domain understanding**

**Recommendation:** Start with `all-MiniLM-L6-v2` (free, fast), upgrade to OpenAI for production

### Text Preprocessing

```python
def prepare_document_for_embedding(paper: dict) -> str:
    """
    Combine title, abstract, and body text with weighting
    """
    title = paper.get("title", "")
    abstract = paper.get("abstract", "")
    body = paper.get("full_text", "")

    # Weight title and abstract more heavily
    text = f"{title} {title} {abstract} {abstract} {body}"

    # Truncate to model's max length
    max_tokens = 512  # For MiniLM
    text = text[:max_tokens * 4]  # Rough token estimate

    return text
```

## Implementation

### Chroma Integration

```python
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

class VectorDatabase:
    def __init__(self, config: VectorDBConfig):
        self.config = config

        # Initialize Chroma client
        self.client = chromadb.PersistentClient(
            path=str(config.storage_path),
            settings=Settings(
                anonymized_telemetry=False
            )
        )

        # Set up embedding function
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=config.embedding_model
        )

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=config.collection_name,
            embedding_function=self.embedding_fn,
            metadata={"description": "Research papers corpus"}
        )

    def add_papers(self, papers: list[dict]):
        """Add papers to vector database"""
        documents = []
        metadatas = []
        ids = []

        for paper in papers:
            # Prepare text for embedding
            text = self.prepare_text(paper)
            documents.append(text)

            # Store metadata
            metadatas.append({
                "title": paper["title"],
                "authors": ",".join(paper.get("authors", [])),
                "year": paper.get("year"),
                "source": paper.get("source"),  # arxiv, pubmed, etc.
                "arxiv_id": paper.get("arxiv_id"),
                "doi": paper.get("doi"),
            })

            # Use paper ID as document ID
            ids.append(paper["id"])

        # Add to collection (automatically generates embeddings)
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def search(self, query: str, n_results: int = 10, filters: dict = None):
        """Semantic search for papers"""
        where = self.build_filters(filters) if filters else None

        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where
        )

        return self.format_results(results)

    def search_similar(self, paper_id: str, n_results: int = 10):
        """Find papers similar to a given paper"""
        # Get the paper's embedding
        results = self.collection.get(
            ids=[paper_id],
            include=["embeddings"]
        )

        if not results["embeddings"]:
            return []

        embedding = results["embeddings"][0]

        # Search using the embedding
        similar = self.collection.query(
            query_embeddings=[embedding],
            n_results=n_results + 1  # +1 to exclude self
        )

        # Remove the original paper
        filtered = {
            "ids": [similar["ids"][0][i] for i in range(len(similar["ids"][0])) if similar["ids"][0][i] != paper_id],
            "distances": [similar["distances"][0][i] for i in range(len(similar["distances"][0])) if similar["ids"][0][i] != paper_id],
            "metadatas": [similar["metadatas"][0][i] for i in range(len(similar["metadatas"][0])) if similar["ids"][0][i] != paper_id]
        }

        return self.format_results({"ids": [filtered["ids"]], "distances": [filtered["distances"]], "metadatas": [filtered["metadatas"]]})

    def build_filters(self, filters: dict) -> dict:
        """Convert filter dict to Chroma where clause"""
        where = {}

        if "year_min" in filters:
            where["year"] = {"$gte": filters["year_min"]}
        if "year_max" in filters:
            where.setdefault("year", {})["$lte"] = filters["year_max"]
        if "source" in filters:
            where["source"] = filters["source"]

        return where if where else None

    def prepare_text(self, paper: dict) -> str:
        """Prepare paper text for embedding"""
        title = paper.get("title", "")
        abstract = paper.get("abstract", "")
        body = paper.get("full_text", "")[:2000]  # Limit body length

        return f"{title} {title} {abstract} {abstract} {body}"

    def format_results(self, results) -> list[dict]:
        """Format Chroma results for consumption"""
        formatted = []
        for i in range(len(results["ids"][0])):
            formatted.append({
                "id": results["ids"][0][i],
                "similarity": 1 - results["distances"][0][i],  # Convert distance to similarity
                "metadata": results["metadatas"][0][i]
            })
        return formatted
```

### Initialization Script

**`server/scripts/init_vector_db.py`:**
```python
import argparse
from pathlib import Path
from vector_db import VectorDatabase, load_config
from pdf_parser import extract_text_from_pdf

def initialize_from_papers_directory(papers_dir: Path):
    """Initialize vector DB with papers from data/papers"""
    config = load_config()
    db = VectorDatabase(config)

    papers = []
    for pdf_path in papers_dir.glob("*.pdf"):
        print(f"Processing {pdf_path.name}...")

        try:
            # Extract text from PDF
            text = extract_text_from_pdf(pdf_path)

            # Create paper document
            paper = {
                "id": pdf_path.stem,  # Filename without extension
                "title": extract_title(text),  # TODO: Implement
                "abstract": extract_abstract(text),  # TODO: Implement
                "full_text": text,
                "source": "local",
                "file_path": str(pdf_path)
            }

            papers.append(paper)

        except Exception as e:
            print(f"Error processing {pdf_path.name}: {e}")
            continue

    # Add to vector database
    print(f"\nAdding {len(papers)} papers to vector database...")
    db.add_papers(papers)

    print("✅ Initialization complete!")
    print(f"Database location: {config.storage_path}")
    print(f"Total papers: {db.collection.count()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--papers-dir",
        type=Path,
        default=Path("../../data/papers"),
        help="Directory containing PDF papers"
    )
    args = parser.parse_args()

    initialize_from_papers_directory(args.papers_dir)
```

**Usage:**
```bash
cd server
python scripts/init_vector_db.py --papers-dir ../data/papers
```

## Testing

### Unit Tests

```python
import pytest
from vector_db import VectorDatabase

@pytest.fixture
def vector_db(tmp_path):
    config = VectorDBConfig(storage_path=tmp_path / "test_chroma")
    return VectorDatabase(config)

def test_add_and_search(vector_db):
    # Add test papers
    papers = [
        {
            "id": "paper1",
            "title": "CRISPR gene editing in bioink scaffolds",
            "abstract": "We demonstrate CRISPR editing...",
            "year": 2023
        },
        {
            "id": "paper2",
            "title": "3D bioprinting of tissue constructs",
            "abstract": "Bioprinting enables...",
            "year": 2022
        }
    ]
    vector_db.add_papers(papers)

    # Search
    results = vector_db.search("CRISPR gene editing", n_results=1)

    assert len(results) == 1
    assert results[0]["id"] == "paper1"
    assert results[0]["similarity"] > 0.7

def test_similar_papers(vector_db):
    # Add papers and test similarity search
    # ...
```

## Monitoring & Analytics

### Metrics to Track

```python
# Add to database class
def get_stats(self) -> dict:
    return {
        "total_papers": self.collection.count(),
        "storage_size_mb": self.get_storage_size(),
        "embedding_model": self.config.embedding_model,
        "embedding_dimension": self.config.dimension
    }
```

### Usage Logging

```python
logger.info("Vector search", extra={
    "query": query[:50],
    "n_results": n_results,
    "filters": filters,
    "results_found": len(results),
    "top_similarity": results[0]["similarity"] if results else 0
})
```

## Migration Path

### Phase 1: Chroma (Current)
- Local development
- Up to 100k documents
- Single machine

### Phase 2: Production Ready
- Add Redis cache layer
- Optimize embedding batch processing
- Monitor performance metrics

### Phase 3: Scale (If Needed)
- Migrate to Weaviate or Qdrant
- Distributed setup
- 1M+ documents

## Related Documentation

- [TASKS.md](TASKS.md) - Phase 0 decision, Phase 1 setup, Phase 2 initialization
- [MCP_INTEGRATION_SPEC.md](MCP_INTEGRATION_SPEC.md) - Document retrieval from APIs
- [PROJECT_STATUS.md](PROJECT_STATUS.md) - Technical decisions tracking

## References

- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
