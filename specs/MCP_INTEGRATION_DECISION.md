# MCP Integration Decision for Document Repositories

**Issue:** [#5](https://github.com/buddha314/babocument/issues/5)
**Created:** 2025-11-06
**Status:** ✅ DECIDED
**Decision:** Hybrid Approach - Use existing community servers with custom extensions

## Executive Summary

After reviewing the Model Context Protocol (MCP) ecosystem, I recommend a **Hybrid Approach** that leverages existing community MCP servers for core functionality while building targeted custom extensions for Babocument-specific features. This balances development speed, maintainability, and customization needs.

## Available Community MCP Servers

### arXiv Integration

**Found in MCP Repository:**
1. **arXiv API** (by prashalruchiranga)
   - Repository: https://github.com/prashalruchiranga/arxiv-mcp-server
   - Status: Active community server
   - Features: Natural language interaction with arXiv API
   - Transport: Standard MCP protocol

2. **arxiv-latex-mcp** (by takashiishida)
   - Repository: https://github.com/takashiishida/arxiv-latex-mcp
   - Status: Active community server
   - Features: Fetches and processes arXiv LaTeX sources for mathematical expressions
   - Special Use Case: Precise interpretation of papers with complex math

**Assessment:**
- ✅ Active community support
- ✅ Natural language interface
- ✅ LaTeX/math support available
- ⚠️ May need extensions for full-text caching
- ⚠️ Rate limiting needs verification

### PubMed/PMC Integration

**Found in MCP Repository:**
1. **BioMCP** (by genomoncology/imaurer)
   - Repository: https://github.com/genomoncology/biomcp
   - Status: Active, biomedical research focused
   - Features:
     - PubMed access
     - ClinicalTrials.gov integration
     - MyVariant.info support
   - Perfect Match: Designed for biomedical research

2. **Entrez** (QuentinCody)
   - Repository: https://github.com/QuentinCody/entrez-mcp-server
   - Status: Community maintained
   - Features: Unofficial MCP for NCBI Entrez (PubMed, genes, proteins)
   - Comprehensive: Covers multiple NCBI databases

**Assessment:**
- ✅ **BioMCP is ideal** - covers PubMed + ClinicalTrials.gov + genetic data
- ✅ Purpose-built for biomedical research (Beabadoo's domain)
- ✅ Maintained by genomoncology (credible organization)
- ✅ Entrez available as backup/alternative

### bioRxiv/medRxiv Integration

**Found in MCP Repository:**
1. **bioRxiv** (by JackKuo666)
   - Repository: https://github.com/JackKuo666/bioRxiv-MCP-Server
   - Status: Active
   - Features: Search and access bioRxiv papers via MCP
   - Simple interface

2. **medRxiv** (by JackKuo666)
   - Repository: https://github.com/JackKuo666/medRxiv-MCP-Server
   - Status: Active
   - Features: Search and access medRxiv papers via MCP
   - Paired with bioRxiv server

**Assessment:**
- ✅ Preprint server coverage
- ✅ Same developer = consistent interface
- ⚠️ May need monitoring for API changes
- Priority: MEDIUM (as specified in original spec)

### Google Scholar

**Found in MCP Repository:**
1. **Google-Scholar** (by JackKuo666 and mochow13)
   - Multiple implementations available
   - TypeScript version with Streamable HTTP transport
   - Gemini integration option

**Assessment:**
- ✅ Backup option for broad coverage
- ⚠️ May have rate limiting issues
- Priority: LOW (use as fallback)

## Recommended Architecture

### Phase 1: Core Integration (Immediate)

```
FastAgent Backend
    ↓
MCP Client
    ↓
├── BioMCP Server (Primary)
│   ├── PubMed
│   ├── ClinicalTrials.gov
│   └── MyVariant.info
│
├── arXiv API Server
│   └── arXiv papers + LaTeX support
│
└── bioRxiv MCP Server
    ├── bioRxiv
    └── medRxiv
```

### Phase 2: Custom Extensions (When Needed)

Build custom MCP servers or tools only for:

1. **Advanced Caching Layer**
   - Full-text paper storage in vector database
   - Semantic search optimization
   - Offline access

2. **Cross-Repository Deduplication**
   - DOI-based matching across sources
   - Citation network integration
   - Unified metadata format

3. **Babocument-Specific Features**
   - Timeline visualization data prep
   - Keyword frequency aggregation
   - Custom analytics for biomanufacturing research

## Implementation Plan

### Step 1: Install and Test Community Servers (Week 1)

#### 1.1 Set Up BioMCP
```bash
# Install BioMCP
pip install biomcp  # or appropriate install command

# Configure in FastAgent
# .mcp/config.json
{
  "mcpServers": {
    "biomcp": {
      "command": "python",
      "args": ["-m", "biomcp"],
      "env": {
        "NCBI_API_KEY": "${NCBI_API_KEY}",  # Free from NCBI
        "RATE_LIMIT_PER_SECOND": "10"
      }
    }
  }
}
```

#### 1.2 Set Up arXiv MCP
```bash
# Install arXiv MCP server
npm install -g arxiv-mcp-server  # or appropriate command

# Configure
{
  "mcpServers": {
    "arxiv": {
      "command": "node",
      "args": ["arxiv-mcp-server"],
      "env": {
        "RATE_LIMIT_PER_SECOND": "0.33"  # 1 req per 3 seconds
      }
    }
  }
}
```

#### 1.3 Set Up bioRxiv/medRxiv MCP
```bash
# Install bioRxiv MCP
npm install -g biorxiv-mcp-server  # or appropriate command

{
  "mcpServers": {
    "biorxiv": {
      "command": "node",
      "args": ["biorxiv-mcp-server"]
    }
  }
}
```

### Step 2: Research Agent Integration (Week 1-2)

Create a unified Research Agent interface:

```python
# research_agent.py
from typing import List, Dict
from fastapi import Depends
from mcp_client import MCPClient

class ResearchAgent:
    def __init__(self, mcp_client: MCPClient):
        self.mcp = mcp_client
        self.sources = {
            'pubmed': 'biomcp',
            'clinicaltrials': 'biomcp',
            'arxiv': 'arxiv',
            'biorxiv': 'biorxiv',
            'medRxiv': 'biorxiv'
        }
    
    async def search_papers(
        self, 
        query: str, 
        sources: List[str] = None,
        max_results: int = 50
    ) -> List[Dict]:
        """Unified search across all document repositories"""
        if sources is None:
            sources = list(self.sources.keys())
        
        results = []
        for source in sources:
            server = self.sources.get(source)
            if not server:
                continue
            
            try:
                # Call appropriate MCP tool
                source_results = await self.mcp.call_tool(
                    server,
                    "search",
                    {
                        "query": query,
                        "max_results": max_results,
                        "sort_by": "relevance"
                    }
                )
                
                # Standardize format
                for result in source_results:
                    results.append({
                        'source': source,
                        'title': result.get('title'),
                        'authors': result.get('authors'),
                        'abstract': result.get('abstract'),
                        'doi': result.get('doi'),
                        'url': result.get('url'),
                        'publication_date': result.get('date'),
                        'metadata': result
                    })
                    
            except Exception as e:
                logger.error(f"Error searching {source}: {e}")
                continue
        
        return self._deduplicate_by_doi(results)
    
    async def get_full_text(self, paper_id: str, source: str) -> str:
        """Retrieve full text from appropriate source"""
        server = self.sources.get(source)
        return await self.mcp.call_tool(
            server,
            "get_full_text",
            {"paper_id": paper_id}
        )
    
    def _deduplicate_by_doi(self, results: List[Dict]) -> List[Dict]:
        """Remove duplicates based on DOI"""
        seen_dois = set()
        deduplicated = []
        
        for result in results:
            doi = result.get('doi')
            if doi and doi in seen_dois:
                continue
            if doi:
                seen_dois.add(doi)
            deduplicated.append(result)
        
        return deduplicated
```

### Step 3: Vector Database Integration (Week 2)

Store retrieved papers in vector database (ChromaDB recommended from Issue #4):

```python
# vector_store.py
import chromadb
from sentence_transformers import SentenceTransformer

class PaperVectorStore:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name="research_papers",
            metadata={"description": "Scientific papers from multiple sources"}
        )
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
    
    async def store_paper(self, paper: Dict):
        """Store paper with embeddings"""
        # Generate embedding from title + abstract
        text = f"{paper['title']} {paper['abstract']}"
        embedding = self.embedder.encode(text).tolist()
        
        self.collection.add(
            ids=[paper['doi'] or paper['url']],
            embeddings=[embedding],
            documents=[paper['abstract']],
            metadatas=[{
                'title': paper['title'],
                'source': paper['source'],
                'date': paper['publication_date'],
                'authors': ','.join(paper['authors']),
                'url': paper['url']
            }]
        )
    
    async def semantic_search(self, query: str, n_results: int = 10):
        """Semantic search across cached papers"""
        query_embedding = self.embedder.encode(query).tolist()
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        return results
```

### Step 4: API Endpoints (Week 2)

Create FastAPI endpoints:

```python
# api/papers.py
from fastapi import APIRouter, Depends
from research_agent import ResearchAgent
from vector_store import PaperVectorStore

router = APIRouter(prefix="/api/papers", tags=["papers"])

@router.post("/search")
async def search_papers(
    query: str,
    sources: List[str] = None,
    use_cache: bool = True,
    agent: ResearchAgent = Depends(get_research_agent)
):
    """Search papers across multiple sources"""
    
    # Try semantic search in cache first
    if use_cache:
        vector_store = PaperVectorStore()
        cached_results = await vector_store.semantic_search(query)
        if cached_results:
            return {"source": "cache", "results": cached_results}
    
    # Fetch from MCP servers
    results = await agent.search_papers(query, sources)
    
    # Cache results
    vector_store = PaperVectorStore()
    for paper in results:
        await vector_store.store_paper(paper)
    
    return {"source": "live", "results": results}

@router.get("/paper/{paper_id}")
async def get_paper(
    paper_id: str,
    source: str,
    agent: ResearchAgent = Depends(get_research_agent)
):
    """Get full paper details"""
    full_text = await agent.get_full_text(paper_id, source)
    return {"paper_id": paper_id, "full_text": full_text}
```

## Decision Rationale

### Why Hybrid Approach?

| Criteria | Community Servers | Custom Servers | Hybrid (Chosen) |
|----------|------------------|----------------|-----------------|
| Development Speed | ⭐⭐⭐⭐⭐ Fast | ⭐⭐ Slow | ⭐⭐⭐⭐ Fast start |
| Maintenance Burden | ⭐⭐⭐⭐ Low | ⭐⭐ High | ⭐⭐⭐ Medium |
| Customization | ⭐⭐ Limited | ⭐⭐⭐⭐⭐ Full | ⭐⭐⭐⭐ Good |
| API Coverage | ⭐⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Complete | ⭐⭐⭐⭐⭐ Best |
| Community Support | ⭐⭐⭐⭐ Strong | ⭐ None | ⭐⭐⭐⭐ Strong |

### Specific Advantages

1. **BioMCP is Purpose-Built**
   - Already integrates PubMed + ClinicalTrials.gov
   - Maintained by genomoncology (credible)
   - Saves weeks of development time

2. **arXiv MCP with LaTeX Support**
   - Mathematical paper parsing is complex
   - Community server already handles it
   - Focus on value-add features instead

3. **Incremental Custom Development**
   - Start with community servers
   - Build custom features only when needed
   - Avoid premature optimization

4. **Reduced Maintenance**
   - API changes handled by community
   - Security updates from upstream
   - Focus on Babocument-specific logic

## Risk Mitigation

### Risk 1: Community Server Abandonment
**Mitigation:**
- Use multiple servers from different developers
- Fork and maintain locally if needed
- Most servers have permissive licenses (MIT/Apache)

### Risk 2: Rate Limiting Issues
**Mitigation:**
- Implement aggressive caching in vector database
- Use NCBI API key for 10 req/sec (vs 3 default)
- Add exponential backoff
- Queue requests across multiple users

### Risk 3: Feature Gaps
**Mitigation:**
- Build custom MCP servers only for gaps
- Extend community servers via pull requests
- Maintain list of required vs nice-to-have features

## Future Custom Development

Build custom MCP servers when:

1. **Advanced Analytics Required**
   - Temporal trend analysis (Issue #8)
   - Cross-repository citation networks
   - Keyword frequency aggregation

2. **Performance Critical**
   - Sub-second response times needed
   - Bulk operations (1000+ papers)
   - Real-time streaming required

3. **Proprietary Features**
   - Babocument-specific UI integration
   - Custom metadata schemas
   - Private data sources

## Testing Strategy

### Week 1: Integration Testing
```bash
# Test each MCP server individually
pytest tests/mcp/test_biomcp.py
pytest tests/mcp/test_arxiv.py
pytest tests/mcp/test_biorxiv.py

# Test unified Research Agent
pytest tests/agents/test_research_agent.py
```

### Week 2: Load Testing
```python
# Test rate limiting
async def test_rate_limits():
    agent = ResearchAgent(mcp_client)
    
    # Should handle burst requests
    tasks = [
        agent.search_papers("biomanufacturing", ["pubmed"])
        for _ in range(20)
    ]
    results = await asyncio.gather(*tasks)
    
    assert all(results)  # No failures
```

### Week 3: End-to-End Testing
```python
# Test complete workflow
async def test_paper_discovery_workflow():
    # Search
    results = await search_papers("CRISPR biomanufacturing")
    
    # Get full text
    paper = results[0]
    full_text = await get_paper(paper['doi'], paper['source'])
    
    # Store in vector DB
    await vector_store.store_paper({**paper, 'full_text': full_text})
    
    # Semantic search
    similar = await vector_store.semantic_search("gene editing")
    
    assert len(similar) > 0
```

## Success Metrics

### Phase 1 (Immediate - 2 weeks)
- ✅ All 3 MCP servers operational
- ✅ Research Agent can query all sources
- ✅ Papers stored in vector database
- ✅ Basic API endpoints working

### Phase 2 (1 month)
- ✅ 95%+ uptime for MCP servers
- ✅ Sub-3-second search response times
- ✅ Cache hit rate > 40%
- ✅ Zero rate limit violations

### Phase 3 (3 months)
- ✅ 1000+ papers cached
- ✅ Semantic search working
- ✅ Custom analytics integrated
- ✅ User feedback positive

## Resources Required

### Development Time
- Week 1-2: MCP server setup and testing
- Week 3-4: Research Agent integration
- Week 5-6: Vector database and caching
- Week 7-8: API endpoints and frontend integration

### External Services
- NCBI API Key (free, registration required)
- No paid services required initially
- Consider Semantic Scholar API for advanced features

### Infrastructure
- Local/cloud server for MCP servers
- ChromaDB instance (from Issue #4)
- Standard FastAgent deployment

## Related Documentation

- Original Spec: [specs/MCP_INTEGRATION_SPEC.md](MCP_INTEGRATION_SPEC.md)
- Vector Database Decision: [specs/VECTOR_DATABASE_SPEC.md](VECTOR_DATABASE_SPEC.md)
- Project Tasks: [specs/TASKS.md](TASKS.md)
- Issue #5: https://github.com/buddha314/babocument/issues/5

## Approval and Sign-off

**Decision:** Approved - Hybrid Approach
**Date:** 2025-11-06
**Next Steps:** Begin Phase 1 implementation (MCP server setup)

---

*This decision can be revisited as we gain experience with the community MCP servers and identify specific needs for custom development.*
