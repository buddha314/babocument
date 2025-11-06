# MCP Integration Specification for Document Repositories

**Created:** 2025-11-06
**Purpose:** Define Model Context Protocol (MCP) integration strategy for accessing research document repositories

## Overview

Babocument will use MCP (Model Context Protocol) servers to provide agents with access to scientific document repositories like arXiv, PubMed, bioRxiv, and others. This enables the Research Agent to query and retrieve full-text papers and metadata from trusted sources.

## What is MCP?

The Model Context Protocol is a standardized way to connect AI assistants (agents) to external data sources and tools. MCP servers expose resources, tools, and prompts that agents can use to access information.

**Key Benefits:**
- Standardized interface for multiple data sources
- Built-in authentication and rate limiting
- Community-maintained servers for popular APIs
- Easy to add new sources without changing agent code
- Separation of concerns (data access vs agent logic)

## Target Document Repositories

### Primary Sources (Must Support)

#### 1. arXiv
**Description:** Open-access preprint repository for physics, math, CS, biology, and more

**Coverage:**
- 2M+ papers across multiple disciplines
- Daily updates
- Full-text PDF and LaTeX source available
- Rich metadata (authors, abstracts, categories)

**API:**
- arXiv API 2.0 (free, no auth required)
- Rate limit: ~1 request/3 seconds
- Bulk access via S3 buckets

**MCP Options:**
- **Community MCP Server:** Check [MCP Server Hub](https://github.com/modelcontextprotocol/servers)
- **Custom Implementation:** Build on arXiv API
- **Recommended:** Use community server if available, otherwise build custom

**Priority:** HIGH (core research repository)

#### 2. PubMed / PubMed Central (PMC)
**Description:** NIH database of biomedical literature

**Coverage:**
- PubMed: 36M+ citations and abstracts
- PMC: 8M+ full-text articles
- Focus: Life sciences, biomedicine, biomanufacturing

**API:**
- E-utilities API (free, no auth for < 3 req/sec)
- Rate limit: 3 req/sec without API key, 10 req/sec with key
- Full-text available for PMC Open Access subset

**MCP Options:**
- **Community MCP Server:** Likely exists (check MCP hub)
- **Custom Implementation:** Use Entrez E-utilities
- **Recommended:** Community server + custom extensions

**Priority:** HIGH (critical for Beabadoo's biomanufacturing research)

#### 3. bioRxiv / medRxiv
**Description:** Preprint servers for biology and medicine

**Coverage:**
- bioRxiv: Biology preprints
- medRxiv: Medical and health sciences preprints
- Rapid dissemination before peer review

**API:**
- bioRxiv API (free)
- Rate limit: Reasonable usage
- Metadata and abstracts available

**MCP Options:**
- **Community MCP Server:** May exist
- **Custom Implementation:** Straightforward REST API
- **Recommended:** Custom implementation (simple API)

**Priority:** MEDIUM (valuable for cutting-edge research)

### Secondary Sources (Optional)

#### 4. Semantic Scholar
- API for 200M+ papers across all fields
- Advanced citation network data
- Research graph features

#### 5. CORE
- Aggregator of open access research
- 240M+ papers from repositories worldwide

#### 6. Europe PMC
- European equivalent of PubMed Central
- Complementary coverage

#### 7. Google Scholar (via SerpAPI)
- Broadest coverage but requires paid API
- Good for citation counts

## MCP Architecture

### Server Selection Strategy

**Option A: Use Community MCP Servers**
```
Agent → MCP Client → Community MCP Server → API (arXiv/PubMed)
```

**Pros:**
- Maintained by community
- Pre-built authentication
- Regular updates

**Cons:**
- Dependency on external maintainers
- May not support all features needed
- Less control over customization

**Option B: Build Custom MCP Servers**
```
Agent → MCP Client → Custom MCP Server → API (arXiv/PubMed)
```

**Pros:**
- Full control over features
- Optimized for our use cases
- Can combine multiple APIs in one server

**Cons:**
- Development and maintenance burden
- Need to handle auth, rate limiting, errors

**Recommended: Hybrid Approach**
1. Use community servers where they exist and are well-maintained
2. Build custom servers for repositories without good MCP support
3. Extend community servers with custom tools if needed

### MCP Server Deployment

**For Development:**
- Run MCP servers locally as separate processes
- Configure in Claude Desktop or agent config file
- Use localhost URLs for connections

**For Production:**
- Deploy MCP servers as containerized services
- Load balancing for multiple servers
- Centralized logging and monitoring

### Configuration Format

**MCP Config File (`.mcp/config.json`):**
```json
{
  "mcpServers": {
    "arxiv": {
      "command": "node",
      "args": ["./mcp-servers/arxiv/index.js"],
      "env": {
        "ARXIV_API_KEY": "${ARXIV_API_KEY}",
        "RATE_LIMIT_PER_SECOND": "0.33"
      }
    },
    "pubmed": {
      "command": "python",
      "args": ["-m", "mcp_pubmed"],
      "env": {
        "NCBI_API_KEY": "${NCBI_API_KEY}",
        "RATE_LIMIT_PER_SECOND": "10"
      }
    },
    "biorxiv": {
      "command": "node",
      "args": ["./mcp-servers/biorxiv/index.js"]
    }
  }
}
```

## Agent Integration

### Research Agent Access Pattern

```python
# Research Agent uses MCP tools
class ResearchAgent:
    def __init__(self, mcp_client):
        self.mcp = mcp_client

    async def search_papers(self, query: str, sources: list[str]):
        results = []

        # Search arXiv via MCP
        if "arxiv" in sources:
            arxiv_results = await self.mcp.call_tool(
                "arxiv",
                "search",
                {
                    "query": query,
                    "max_results": 50,
                    "sort_by": "relevance"
                }
            )
            results.extend(arxiv_results)

        # Search PubMed via MCP
        if "pubmed" in sources:
            pubmed_results = await self.mcp.call_tool(
                "pubmed",
                "search",
                {
                    "query": query,
                    "max_results": 50,
                    "filter": "full_text_available"
                }
            )
            results.extend(pubmed_results)

        return self.deduplicate_and_rank(results)

    async def fetch_full_text(self, paper_id: str, source: str):
        """Retrieve full text of a paper"""
        return await self.mcp.call_tool(
            source,
            "get_full_text",
            {"paper_id": paper_id}
        )
```

### MCP Tools to Implement

**For Each Repository Server:**

#### Tool: `search`
```typescript
{
  name: "search",
  description: "Search for papers by keyword, author, or topic",
  inputSchema: {
    query: string,
    max_results?: number,
    sort_by?: "relevance" | "date" | "citations",
    date_range?: { start: string, end: string }
  }
}
```

#### Tool: `get_metadata`
```typescript
{
  name: "get_metadata",
  description: "Get metadata for a specific paper",
  inputSchema: {
    paper_id: string
  }
}
```

#### Tool: `get_full_text`
```typescript
{
  name: "get_full_text",
  description: "Download full text (PDF or plain text)",
  inputSchema: {
    paper_id: string,
    format?: "pdf" | "text"
  }
}
```

#### Tool: `get_citations`
```typescript
{
  name: "get_citations",
  description: "Get papers that cite this paper",
  inputSchema: {
    paper_id: string,
    max_results?: number
  }
}
```

#### Tool: `get_references`
```typescript
{
  name: "get_references",
  description: "Get papers referenced by this paper",
  inputSchema: {
    paper_id: string
  }
}
```

## Data Pipeline

### Document Retrieval Flow

```
User Query
    ↓
Research Agent
    ↓
MCP Client (call_tool)
    ↓
MCP Server (arXiv/PubMed/etc)
    ↓
External API
    ↓
MCP Server (process response)
    ↓
Research Agent (receive results)
    ↓
Vector Database (store for future search)
    ↓
Return to User
```

### Caching Strategy

**Level 1: MCP Server Cache**
- Cache API responses (5 minutes - 1 hour)
- Reduce API calls
- Handle rate limiting

**Level 2: Vector Database**
- Store full-text papers long-term
- Enable semantic search
- Offline access

**Level 3: Application Cache**
- Cache processed results
- Recent queries (1 hour)
- Hot papers (frequently accessed)

## Rate Limiting & Ethics

### Respect API Limits

**arXiv:**
- Maximum 1 request per 3 seconds
- Use bulk access for large downloads
- Identify requests with User-Agent

**PubMed:**
- 3 requests/second without key
- 10 requests/second with API key
- Register for API key (free)

**bioRxiv:**
- "Reasonable usage"
- Implement exponential backoff
- Cache aggressively

### Implementation

```python
import asyncio
from collections import deque
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_calls: int, time_window: timedelta):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = deque()

    async def acquire(self):
        now = datetime.now()

        # Remove old calls outside time window
        while self.calls and self.calls[0] < now - self.time_window:
            self.calls.popleft()

        # Wait if at limit
        if len(self.calls) >= self.max_calls:
            wait_time = (self.calls[0] + self.time_window - now).total_seconds()
            await asyncio.sleep(wait_time)

        self.calls.append(now)

# Usage
arxiv_limiter = RateLimiter(max_calls=1, time_window=timedelta(seconds=3))
pubmed_limiter = RateLimiter(max_calls=10, time_window=timedelta(seconds=1))
```

## Error Handling

### Common Errors

1. **Rate Limit Exceeded**
   - Retry with exponential backoff
   - Queue requests
   - Inform user of delay

2. **Paper Not Found**
   - Return empty result gracefully
   - Log for analytics
   - Suggest alternative sources

3. **API Unavailable**
   - Fallback to other sources
   - Use cached data if available
   - Notify user of degraded service

4. **Full Text Not Available**
   - Return abstract only
   - Provide external link
   - Check alternative repositories

### Implementation

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def fetch_with_retry(url: str):
    try:
        response = await http_client.get(url)
        response.raise_for_status()
        return response.json()
    except HTTPStatusError as e:
        if e.response.status_code == 429:
            # Rate limited - retry
            raise
        elif e.response.status_code == 404:
            # Not found - don't retry
            return None
        else:
            # Other error - retry
            raise
```

## Development Roadmap

### Phase 1: MCP Server Setup (Week 1-2)
- [ ] Research available community MCP servers
- [ ] Test arXiv MCP server integration
- [ ] Test PubMed MCP server integration
- [ ] Build custom servers for gaps
- [ ] Configure MCP client in FastAgent

### Phase 2: Agent Integration (Week 3-4)
- [ ] Implement Research Agent MCP tools access
- [ ] Add search functionality via MCP
- [ ] Add full-text retrieval
- [ ] Implement caching layer
- [ ] Add rate limiting

### Phase 3: Advanced Features (Week 5-6)
- [ ] Citation network traversal
- [ ] Cross-repository deduplication
- [ ] Metadata enrichment
- [ ] User preference learning

## Testing Strategy

### Unit Tests
- Mock MCP server responses
- Test rate limiting logic
- Verify error handling

### Integration Tests
- Real API calls (use test accounts)
- End-to-end paper retrieval
- Cache invalidation

### Load Tests
- Concurrent request handling
- Rate limit compliance
- Failover scenarios

## Security & Privacy

### API Keys
- Store in environment variables
- Never commit to git
- Rotate periodically

### User Data
- Don't store personal searches on external APIs
- Anonymize query logs
- Comply with GDPR/CCPA

### Paper Copyright
- Respect open access licenses
- Only full-text from legal sources
- Link to publisher for paywalled content

## Monitoring & Analytics

### Metrics to Track
- API call counts by source
- Rate limit hits
- Cache hit rates
- Error rates by source
- Average response times
- Papers retrieved per query

### Logging
```python
logger.info("MCP call", extra={
    "server": "arxiv",
    "tool": "search",
    "query": query_hash,  # Hashed for privacy
    "results": len(results),
    "cache_hit": False,
    "duration_ms": 234
})
```

## Alternative Approaches

### Direct API Integration (No MCP)
**If MCP proves too complex:**
- Implement direct API clients for each source
- Use standard HTTP libraries
- Less standardized but more direct control

### Unified Search Service
**Aggregate APIs into single service:**
- Build custom search aggregator
- Single endpoint for all sources
- Internal rate limiting and caching

## References

- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [MCP Server Examples](https://github.com/modelcontextprotocol/servers)
- [arXiv API Documentation](https://info.arxiv.org/help/api/index.html)
- [PubMed E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
- [bioRxiv API](https://api.biorxiv.org/)

## Related Documentation

- [TASKS.md](TASKS.md) - Phase 0 MCP decision, Phase 2 implementation
- [VECTOR_DATABASE_SPEC.md](VECTOR_DATABASE_SPEC.md) - Complementary storage
- [PROJECT_STATUS.md](PROJECT_STATUS.md) - Technical decisions tracking
