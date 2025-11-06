# Multi-Agent Architecture Design

**Decision Status:** ✅ RECOMMENDED - Event-Driven Coordinator Pattern
**Date:** 2025-11-06
**Context:** Issue #2

## Executive Summary

**Recommendation:** Implement an **event-driven coordinator pattern** with specialized agents using FastAgent framework, coordinated through a central Agent Coordinator with Redis pub/sub for scalability.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Client (BabylonJS)                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────────┐  │
│  │   REST   │  │WebSocket │  │   Librarian Character     │  │
│  │   API    │  │ /ws/     │  │   (User Interface)        │  │
│  └─────┬────┘  └─────┬────┘  └────────────┬──────────────┘  │
└────────┼─────────────┼────────────────────┼─────────────────┘
         │             │                    │
         │             │                    │
┌────────┼─────────────┼────────────────────┼─────────────────┐
│        │             │                    │                  │
│   ┌────▼────────────▼────────────────────▼──────┐           │
│   │        FastAPI Server Layer                 │           │
│   │  ┌──────────────────────────────────────┐   │           │
│   │  │      Agent Coordinator               │   │           │
│   │  │  - Request routing                   │   │           │
│   │  │  - Agent lifecycle management        │   │           │
│   │  │  - Event bus (Redis pub/sub)         │   │           │
│   │  │  - State management                  │   │           │
│   │  │  - Task queue (Celery)               │   │           │
│   │  └──┬───────────┬────────────┬─────────┬────┘           │
│   └─────┼───────────┼────────────┼─────────┼────────────────┘
│         │           │            │         │                 │
│    ┌────▼────┐ ┌───▼─────┐ ┌───▼──────┐ ┌▼────────┐ ┌──────▼───────┐  │
│    │Research │ │Analysis │ │ Summary  │ │WebSearch│ │Recommendation│  │
│    │ Agent   │ │ Agent   │ │  Agent   │ │ Agent   │ │    Agent     │  │
│    └────┬────┘ └───┬─────┘ └───┬──────┘ └─┬───────┘ └──────┬───────┘  │
│         │          │            │               │           │
│    ┌────▼──────────▼────────────▼───────────────▼───────┐  │
│    │            Shared Resources                         │  │
│    │  ┌─────────────┐  ┌──────────┐  ┌──────────────┐   │  │
│    │  │Vector DB    │  │  MCP     │  │  LLM         │   │  │
│    │  │(Chroma)     │  │ Servers  │  │ (Ollama)     │   │  │
│    │  └─────────────┘  └──────────┘  └──────────────┘   │  │
│    └────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Agent Definitions

### 1. Agent Coordinator (Core Orchestrator)

**Role:** Central coordinator and request router

**Responsibilities:**
- Accept incoming requests from API/WebSocket
- Route requests to appropriate specialized agents
- Manage agent lifecycle and health
- Coordinate multi-agent workflows
- Publish events to WebSocket clients
- Handle task persistence and recovery

**Communication:**
- Receives: Client requests via REST/WebSocket
- Sends: Task assignments to agents via event bus
- Publishes: Status updates to clients

**Implementation:**
```python
class AgentCoordinator:
    def __init__(self, redis_client, vector_db, llm_client, search_api_client):
        self.agents = {
            'research': ResearchAgent(redis_client, vector_db),
            'analysis': AnalysisAgent(redis_client, vector_db),
            'summary': SummaryAgent(redis_client, llm_client),
            'websearch': WebSearchAgent(redis_client, search_api_client),
            'recommendation': RecommendationAgent(redis_client, vector_db)
        }
        self.event_bus = EventBus(redis_client)
        self.task_queue = TaskQueue(redis_client)

    async def handle_request(self, request: AgentRequest):
        # Determine which agent(s) to invoke
        task_id = str(uuid.uuid4())

        # Publish start event
        await self.event_bus.publish('task.started', {
            'task_id': task_id,
            'type': request.type
        })

        # Route to agent
        if request.type == 'search':
            result = await self.agents['research'].search(request, task_id)
        elif request.type == 'analyze':
            result = await self.agents['analysis'].analyze(request, task_id)
        elif request.type == 'websearch':
            result = await self.agents['websearch'].search(request, task_id)
        # ... etc

        # Publish completion
        await self.event_bus.publish('task.completed', {
            'task_id': task_id,
            'result': result
        })

        return result
```

### 2. Research Agent

**Role:** Query understanding and multi-source document retrieval

**Responsibilities:**
- Parse and understand user research queries
- Search vector database for relevant papers
- Query MCP servers (arXiv, PubMed, bioRxiv)
- Search ClinicalTrials.gov
- Rank and filter results by relevance
- Return structured result sets

**Inputs:**
```typescript
{
  "query": "bioink optimization for 3D printing",
  "filters": {
    "date_range": ["2020-01-01", "2025-11-06"],
    "sources": ["arxiv", "pubmed"],
    "max_results": 50
  }
}
```

**Outputs:**
```typescript
{
  "task_id": "search_123",
  "results": [
    {
      "id": "arxiv:2401.12345",
      "title": "Novel Bioink Formulations...",
      "authors": [...],
      "abstract": "...",
      "relevance_score": 0.94,
      "source": "arxiv",
      "published_date": "2024-01-15"
    }
  ],
  "total_found": 127,
  "search_time_ms": 450
}
```

**Communication Pattern:**
- Subscribes to: `query.search.*` events
- Publishes: `search.progress`, `search.complete` events
- Accesses: Vector DB, MCP servers

### 3. Analysis Agent

**Role:** Trend analysis and data visualization generation

**Responsibilities:**
- Analyze corpus for keyword trends over time
- Generate word clouds from document sets
- Create keyword frequency time series
- Identify correlation patterns
- Compute temporal trends
- Prepare data for Plotly.js visualization

**Inputs:**
```typescript
{
  "analysis_type": "keyword_trends",
  "document_ids": ["arxiv:123", "pubmed:456"],
  "keywords": ["bioink", "scaffold", "3D printing"],
  "time_granularity": "monthly"
}
```

**Outputs:**
```typescript
{
  "task_id": "analysis_789",
  "type": "keyword_trends",
  "data": {
    "timeseries": [
      {
        "date": "2020-01",
        "bioink": 45,
        "scaffold": 32,
        "3D printing": 28
      }
    ],
    "word_cloud": {
      "bioink": 450,
      "collagen": 320,
      "gelatin": 280
      // ... frequency counts
    },
    "correlations": [
      {"term1": "bioink", "term2": "collagen", "r": 0.85}
    ]
  }
}
```

**Communication Pattern:**
- Subscribes to: `query.analyze.*` events
- Publishes: `analysis.progress`, `analysis.complete` events
- Accesses: Vector DB for corpus analysis

### 4. Summary Agent

**Role:** Article summarization and insight extraction

**Responsibilities:**
- Generate concise summaries of research papers
- Extract key findings and contributions
- Identify methodology and results
- Create workspace summaries
- Synthesize multi-document insights

**Inputs:**
```typescript
{
  "summary_type": "article",
  "document_id": "arxiv:2401.12345",
  "max_length": 200,
  "focus_areas": ["methodology", "results"]
}
```

**Outputs:**
```typescript
{
  "task_id": "summary_456",
  "summary": "This paper presents a novel bioink formulation...",
  "key_findings": [
    "35% improvement in cell viability",
    "Novel gelatin-alginate composite"
  ],
  "methodology": "In vitro testing with...",
  "limitations": ["Small sample size", "Single cell line"],
  "confidence": 0.89
}
```

**Communication Pattern:**
- Subscribes to: `query.summarize.*` events
- Publishes: `summary.progress`, `summary.complete` events
- Accesses: LLM for text generation

### 5. Web Search Agent

**Role:** General web search for scientific topics and emerging research

**Responsibilities:**
- Search the open web for scientific content
- Find recent news, blog posts, and preprints
- Discover emerging topics and trends
- Search scientific websites and repositories
- Extract and normalize web content
- Complement academic database searches

**Inputs:**
```typescript
{
  "search_type": "web",
  "query": "latest developments in bioink 3D printing",
  "filters": {
    "date_range": "past_year",
    "domains": ["nature.com", "science.org", "*.edu"],
    "content_type": ["articles", "news", "preprints"]
  },
  "max_results": 20
}
```

**Outputs:**
```typescript
{
  "task_id": "websearch_456",
  "results": [
    {
      "url": "https://nature.com/articles/...",
      "title": "Breakthrough in Bioink Stability...",
      "snippet": "Researchers have developed...",
      "published_date": "2025-10-15",
      "source_domain": "nature.com",
      "content_type": "article",
      "relevance_score": 0.89
    }
  ],
  "search_time_ms": 320
}
```

**Communication Pattern:**
- Subscribes to: `query.websearch.*` events
- Publishes: `websearch.progress`, `websearch.complete` events
- Accesses: Web search APIs (Google Scholar, Bing Academic, etc.)

**Implementation:**
```python
class WebSearchAgent(BaseAgent):
    def __init__(self, redis_client, search_api_client):
        super().__init__(redis_client)
        self.search_client = search_api_client

    async def search(self, query: str, filters: dict, task_id: str):
        # Publish progress
        await self.publish_progress(task_id, 10, "Starting web search...")

        # Execute web search
        raw_results = await self.search_client.search(
            query=query,
            date_range=filters.get('date_range'),
            domains=filters.get('domains')
        )

        # Filter and rank results
        filtered = self._filter_scientific_content(raw_results)
        ranked = self._rank_by_relevance(filtered, query)

        # Publish progress
        await self.publish_progress(task_id, 80, "Processing results...")

        # Extract key information
        enriched_results = await self._enrich_results(ranked)

        return {
            "task_id": task_id,
            "results": enriched_results,
            "total_found": len(raw_results),
            "search_time_ms": self.timer.elapsed_ms()
        }

    def _filter_scientific_content(self, results):
        # Filter for scientific content
        scientific_domains = ['.edu', '.gov', 'nature.com', 'science.org', 'arxiv.org']
        return [r for r in results if any(d in r['url'] for d in scientific_domains)]

    def _rank_by_relevance(self, results, query):
        # Rank by relevance using embeddings
        # Can use vector similarity between query and result snippets
        return sorted(results, key=lambda x: x.get('relevance_score', 0), reverse=True)
```

### 6. Recommendation Agent

**Role:** Related paper suggestions and research gap identification

**Responsibilities:**
- Find related papers based on current reading
- Identify research gaps in corpus
- Suggest next research directions
- Track citation networks
- Identify emerging topics

**Inputs:**
```typescript
{
  "recommendation_type": "related_papers",
  "context": {
    "current_paper_ids": ["arxiv:123"],
    "workspace_id": "workspace_abc",
    "user_interests": ["bioprinting", "tissue engineering"]
  },
  "count": 10
}
```

**Outputs:**
```typescript
{
  "task_id": "rec_789",
  "recommendations": [
    {
      "paper_id": "arxiv:456",
      "title": "Advanced Bioprinting...",
      "relevance_score": 0.92,
      "reason": "Similar methodology, cited by current paper"
    }
  ],
  "research_gaps": [
    "Limited work on long-term stability",
    "Few studies on multi-material printing"
  ]
}
```

**Communication Pattern:**
- Subscribes to: `query.recommend.*` events
- Publishes: `recommendation.complete` events
- Accesses: Vector DB, citation graphs

## Communication Patterns

### Event-Driven Architecture

**Event Bus (Redis Pub/Sub):**
```python
class EventBus:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.pubsub = redis_client.pubsub()

    async def publish(self, channel: str, message: dict):
        await self.redis.publish(channel, json.dumps(message))

    async def subscribe(self, pattern: str, handler: Callable):
        await self.pubsub.psubscribe(pattern)
        async for message in self.pubsub.listen():
            await handler(json.loads(message['data']))
```

**Event Channels:**
- `task.started` - New task initiated
- `task.progress.<task_id>` - Progress updates
- `task.completed.<task_id>` - Task finished
- `task.failed.<task_id>` - Task error
- `agent.health.*` - Agent health status

### Multi-Agent Workflows

**Example: Comprehensive Research Request**

```python
async def comprehensive_research(query: str):
    # 1. Research Agent: Find papers
    search_result = await coordinator.delegate('research', {
        'query': query
    })

    # 2. Analysis Agent: Analyze trends (parallel)
    # 3. Summary Agent: Summarize top papers (parallel)
    async with TaskGroup() as tg:
        analysis_task = tg.create_task(
            coordinator.delegate('analysis', {
                'document_ids': search_result.top_ids
            })
        )
        summary_task = tg.create_task(
            coordinator.delegate('summary', {
                'document_ids': search_result.top_ids[:5]
            })
        )

    # 4. Recommendation Agent: Find related work
    recommendations = await coordinator.delegate('recommendation', {
        'context': search_result.top_ids
    })

    return {
        'search': search_result,
        'analysis': analysis_task.result(),
        'summaries': summary_task.result(),
        'recommendations': recommendations
    }
```

## State Management

### Centralized State Store (Redis)

**Task State:**
```python
task_state = {
    "task_id": "search_123",
    "type": "search",
    "status": "processing",  # pending, processing, completed, failed
    "progress": 45,  # percentage
    "started_at": "2025-11-06T10:30:00Z",
    "updated_at": "2025-11-06T10:30:45Z",
    "agent": "research",
    "result": None,  # populated on completion
    "error": None    # populated on failure
}
```

**Workspace State:**
```python
workspace_state = {
    "workspace_id": "ws_abc",
    "user_id": "user_123",
    "documents": ["arxiv:123", "pubmed:456"],
    "active_queries": ["bioink", "scaffold"],
    "created_at": "2025-11-05T14:00:00Z",
    "updated_at": "2025-11-06T10:30:00Z"
}
```

**Conversation Context (for Librarian):**
```python
conversation_context = {
    "session_id": "sess_xyz",
    "user_id": "user_123",
    "messages": [
        {"role": "user", "content": "Find papers on bioinks"},
        {"role": "assistant", "content": "I found 50 papers..."}
    ],
    "active_workspace": "ws_abc",
    "last_interaction": "2025-11-06T10:30:00Z"
}
```

### State Persistence

- **Short-term (Redis):** Active tasks, sessions, caches
- **Long-term (PostgreSQL):** Workspaces, user data, analytics
- **Vector DB (Chroma):** Document embeddings, semantic search

## Technology Stack

### Backend Framework
```python
# requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
redis==5.0.1
celery==5.3.4
pydantic==2.5.0
httpx==0.25.2  # for MCP client requests
```

### Agent Framework

**Option A: Custom FastAgent Implementation (RECOMMENDED)**
- Full control over architecture
- Optimized for our use case
- Lightweight, no framework overhead

**Option B: LangGraph**
- Built-in state management
- Graph-based workflows
- More complex, steeper learning curve

**Decision:** Start with custom FastAgent, migrate to LangGraph if complexity increases

### Task Queue (Celery)

For long-running tasks:
```python
from celery import Celery

app = Celery('babocument', broker='redis://localhost:6379/0')

@app.task
def long_running_search(query: str, task_id: str):
    # Execute search
    result = perform_search(query)

    # Update state
    redis_client.set(f'task:{task_id}:result', json.dumps(result))

    # Publish event
    event_bus.publish(f'task.completed.{task_id}', result)

    return result
```

## Scalability Considerations

### Horizontal Scaling

**Agent Instances:**
- Multiple instances of each agent type
- Load balanced via Redis queue
- Stateless agent workers

**Event Bus:**
- Redis Cluster for high availability
- Pub/sub for real-time events
- Queue for reliable task delivery

### Performance Optimizations

1. **Caching:**
   - Cache frequent queries in Redis
   - Cache embeddings and search results
   - TTL-based invalidation

2. **Batching:**
   - Batch embedding generation
   - Batch vector searches
   - Batch LLM requests

3. **Async Processing:**
   - All I/O operations async (httpx, aioredis)
   - Parallel agent execution
   - Non-blocking WebSocket updates

## Error Handling & Resilience

### Retry Logic
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def call_mcp_server(query: str):
    # MCP request with retries
    pass
```

### Circuit Breaker
```python
from pybreaker import CircuitBreaker

mcp_breaker = CircuitBreaker(
    fail_max=5,
    timeout_duration=60
)

@mcp_breaker
async def fetch_from_arxiv(query: str):
    # Protected external call
    pass
```

### Graceful Degradation

- If MCP server fails → use cached results
- If LLM fails → return extracted text only
- If vector DB slow → return top results early

## Monitoring & Observability

### Metrics
```python
from prometheus_client import Counter, Histogram

task_counter = Counter('agent_tasks_total', 'Total tasks', ['agent', 'status'])
task_duration = Histogram('agent_task_duration_seconds', 'Task duration', ['agent'])

# Usage
task_counter.labels(agent='research', status='completed').inc()
task_duration.labels(agent='research').observe(task_time)
```

### Logging
```python
import structlog

logger = structlog.get_logger()

logger.info('task_started', task_id=task_id, agent='research', query=query)
logger.info('task_completed', task_id=task_id, duration=duration, result_count=len(results))
```

## API Contract

### REST Endpoints
```
POST /api/v1/tasks/search
POST /api/v1/tasks/websearch
POST /api/v1/tasks/analyze
POST /api/v1/tasks/summarize
POST /api/v1/tasks/recommend
GET  /api/v1/tasks/{task_id}
DELETE /api/v1/tasks/{task_id}
```

### WebSocket Events
```typescript
// Client -> Server
{
  "action": "search",
  "params": { "query": "..." }
}

// Server -> Client
{
  "type": "task.progress",
  "task_id": "search_123",
  "progress": 45,
  "message": "Searching arXiv..."
}

{
  "type": "task.completed",
  "task_id": "search_123",
  "result": { ... }
}
```

## Directory Structure

```
server/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── config.py               # Configuration
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base.py             # Base agent class
│   │   ├── coordinator.py      # Agent coordinator
│   │   ├── research.py         # Research agent
│   │   ├── analysis.py         # Analysis agent
│   │   ├── summary.py          # Summary agent
│   │   ├── websearch.py        # Web search agent
│   │   └── recommendation.py   # Recommendation agent
│   ├── api/
│   │   ├── __init__.py
│   │   ├── rest.py             # REST endpoints
│   │   └── websocket.py        # WebSocket handlers
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py             # Task models
│   │   └── document.py         # Document models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── vector_db.py        # Vector DB client
│   │   ├── mcp_client.py       # MCP client
│   │   └── llm_client.py       # LLM client
│   └── utils/
│       ├── __init__.py
│       ├── event_bus.py        # Redis pub/sub
│       └── state_manager.py    # State management
├── tests/
├── requirements.txt
└── README.md
```

## Implementation Phases

### Phase 1: Foundation (Week 1-2)
- ✅ Set up FastAPI server
- ✅ Implement Agent Coordinator
- ✅ Create base agent class
- ✅ Set up Redis event bus
- ✅ Basic REST endpoints

### Phase 2: Core Agents (Week 3-4)
- ✅ Research Agent (vector DB + MCP)
- ✅ Analysis Agent (trend analysis)
- ✅ Summary Agent (LLM integration)

### Phase 3: Advanced Features (Week 5-6)
- ✅ Recommendation Agent
- ✅ Multi-agent workflows
- ✅ WebSocket real-time updates

### Phase 4: Optimization (Week 7+)
- ✅ Caching and performance tuning
- ✅ Monitoring and observability
- ✅ Error handling and resilience

## Decision Rationale

**Why Event-Driven Coordinator Pattern:**

1. **Scalability** - Agents can scale independently
2. **Flexibility** - Easy to add new agent types
3. **Resilience** - Failure isolation between agents
4. **Real-time** - Natural fit for WebSocket updates
5. **Testability** - Agents can be tested independently
6. **Maintainability** - Clear separation of concerns

## References

- specs/TASKS.md (Phase 5: Agent Intelligence)
- specs/PROJECT_STATUS.md (Agent architecture requirements)
- specs/COMMUNICATION_PROTOCOL_DECISION.md (REST + WebSocket)
- FastAPI documentation: https://fastapi.tiangolo.com/
- Redis pub/sub: https://redis.io/docs/manual/pubsub/

## Next Steps

1. ✅ Document decision (this file)
2. Create base agent class implementation
3. Set up Redis and event bus
4. Implement Agent Coordinator
5. Build Research Agent prototype
6. Update GitHub issue #2 with decision
