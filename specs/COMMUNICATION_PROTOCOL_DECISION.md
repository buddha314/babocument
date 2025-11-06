# Communication Protocol Decision: WebSockets vs REST

**Decision Status:** ✅ RECOMMENDED - Hybrid Approach
**Date:** 2025-11-06
**Context:** Issue #1

## Executive Summary

**Recommendation:** Implement a **hybrid approach** using REST for standard operations and WebSockets for real-time agent updates.

## Analysis

### Requirements Analysis

Based on project specifications:

1. **Real-time agent updates** - Users need live feedback as agents process requests
2. **Document retrieval** - Standard CRUD operations for documents/workspaces
3. **Long-running operations** - Literature searches, embeddings, analysis can take minutes
4. **Interactive chat** - User conversations with Librarian character
5. **Data visualization updates** - Live updates to charts and trends
6. **Multi-user potential** - Future collaboration features

### Option A: Pure REST API

**Architecture:**
```
Client -> HTTP Request -> FastAPI -> Response
         Poll for updates
```

**Pros:**
- Simple to implement and debug
- Standard HTTP tooling (Postman, curl, browser DevTools)
- Easy authentication with JWT tokens
- Stateless, scales horizontally
- Better for caching (CDN, browser cache)

**Cons:**
- Polling required for real-time updates (inefficient)
- Higher latency for streaming responses
- More complex client-side state management
- Poor UX for long-running operations
- Bandwidth waste with polling

**Best for:**
- CRUD operations (create/read/update/delete workspaces, documents)
- File uploads/downloads
- Authentication
- Static content serving

### Option B: Pure WebSockets

**Architecture:**
```
Client <-> WebSocket Connection <-> FastAPI WebSocket endpoint
```

**Pros:**
- True bidirectional real-time communication
- Low latency for updates
- Efficient for streaming data
- Single connection for all communication
- Great for agent status updates

**Cons:**
- More complex to implement and debug
- Connection management overhead
- Harder to scale (sticky sessions)
- No standard HTTP caching
- More difficult error handling
- Debugging tools less mature
- Requires connection keep-alive logic

**Best for:**
- Real-time agent status updates
- Live chat with Librarian
- Streaming agent responses
- Collaborative features (future)
- Live visualization updates

### Option C: Hybrid Approach (RECOMMENDED)

**Architecture:**
```
REST API (FastAPI):
- /api/workspaces/*
- /api/documents/*
- /api/auth/*
- /api/search

WebSocket:
- /ws/agents (agent task updates)
- /ws/chat (Librarian interaction)
- /ws/visualization (live chart updates)
```

**Implementation:**
```python
# FastAPI server
from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse

app = FastAPI()

# REST endpoints
@app.post("/api/search")
async def search_documents(query: SearchQuery):
    task_id = await agents.start_search(query)
    return {"task_id": task_id, "status": "started"}

@app.get("/api/search/{task_id}")
async def get_search_status(task_id: str):
    return await agents.get_task_status(task_id)

# WebSocket for real-time updates
@app.websocket("/ws/agents")
async def agent_websocket(websocket: WebSocket):
    await websocket.accept()
    async for message in websocket.iter_text():
        # Handle agent commands
        # Send real-time updates back
        await websocket.send_json({
            "type": "agent_update",
            "task_id": task_id,
            "status": "processing",
            "progress": 45
        })
```

**Client implementation:**
```typescript
// REST for standard operations
const searchResults = await fetch('/api/search', {
  method: 'POST',
  body: JSON.stringify({ query: 'bioreactor optimization' })
});

// WebSocket for real-time updates
const ws = new WebSocket('ws://localhost:8000/ws/agents');
ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  if (update.type === 'agent_update') {
    updateUI(update);
  }
};
```

## Decision Matrix

| Criterion | REST | WebSockets | Hybrid | Weight |
|-----------|------|------------|--------|--------|
| Real-time updates | ❌ Poor | ✅ Excellent | ✅ Excellent | HIGH |
| Implementation complexity | ✅ Simple | ❌ Complex | ⚠️ Moderate | MEDIUM |
| Debugging/tooling | ✅ Excellent | ❌ Poor | ✅ Good | MEDIUM |
| Scalability | ✅ Excellent | ⚠️ Moderate | ✅ Good | HIGH |
| Agent streaming | ❌ Poor | ✅ Excellent | ✅ Excellent | HIGH |
| CRUD operations | ✅ Excellent | ⚠️ Moderate | ✅ Excellent | MEDIUM |
| Development speed | ✅ Fast | ❌ Slow | ⚠️ Moderate | HIGH |
| Bandwidth efficiency | ❌ Poor | ✅ Excellent | ✅ Good | LOW |

**Score:** Hybrid approach wins on all critical criteria

## Recommended Implementation

### Phase 1: REST Foundation
Start with REST API for:
- Authentication (`POST /api/auth/login`)
- Workspace CRUD (`/api/workspaces/*`)
- Document operations (`/api/documents/*`)
- Search initiation (`POST /api/search`)

### Phase 2: Add WebSocket Layer
Add WebSockets for:
- Agent task updates (`/ws/agents`)
- Live status streaming
- Progress notifications

### Phase 3: Expand Real-time Features
- Chat with Librarian (`/ws/chat`)
- Live visualization updates (`/ws/visualization`)
- Collaborative features (future)

## Technical Specifications

### REST API Structure
```
/api/v1/
  /auth/
    POST /login
    POST /logout
    POST /refresh
  /workspaces/
    GET / (list)
    POST / (create)
    GET /{id}
    PUT /{id}
    DELETE /{id}
  /documents/
    GET / (list with filters)
    GET /{id}
    POST / (upload)
    DELETE /{id}
  /search/
    POST / (initiate search)
    GET /{task_id} (get status)
  /agents/
    GET /status (list all agent tasks)
    POST /cancel/{task_id}
```

### WebSocket Events
```typescript
// Client -> Server
{
  "type": "subscribe",
  "task_id": "search_123"
}

{
  "type": "agent_command",
  "action": "search",
  "params": { "query": "..." }
}

// Server -> Client
{
  "type": "agent_update",
  "task_id": "search_123",
  "status": "processing",
  "progress": 45,
  "message": "Searching arXiv..."
}

{
  "type": "agent_complete",
  "task_id": "search_123",
  "result": { ... }
}

{
  "type": "error",
  "task_id": "search_123",
  "error": "Rate limit exceeded"
}
```

## Implementation Libraries

### Backend (Python/FastAPI)
```python
# requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
websockets==12.0
python-multipart==0.0.6
```

### Frontend (TypeScript/Next.js)
```typescript
// Already available in Next.js
// Native WebSocket API
// Or use: socket.io-client for reconnection logic
```

## Migration Path

1. **Week 1-2:** Implement REST API foundation
2. **Week 3:** Add WebSocket infrastructure
3. **Week 4:** Migrate agent updates to WebSocket
4. **Week 5+:** Add chat and visualization streams

## Decision Rationale

The hybrid approach provides:

1. **Best of both worlds** - REST for standard ops, WS for real-time
2. **Incremental implementation** - Can start with REST, add WS later
3. **Proven pattern** - Used by Slack, Discord, GitHub, etc.
4. **Developer experience** - Easy debugging with standard REST tools
5. **User experience** - Real-time updates without polling
6. **Future-proof** - Supports collaboration features
7. **FastAPI native support** - Both REST and WS supported out-of-box

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| WebSocket connection drops | Implement auto-reconnect with exponential backoff |
| Scaling WebSocket connections | Use Redis pub/sub for multi-server deployments |
| Complex state management | Use task IDs to correlate REST and WS messages |
| Debugging difficulty | Log all WS messages, provide REST fallback endpoints |

## References

- FastAPI WebSocket documentation: https://fastapi.tiangolo.com/advanced/websockets/
- Next.js WebSocket integration patterns
- specs/TASKS.md (Phase 1 requirements)
- specs/PROJECT_STATUS.md (architectural context)

## Next Steps

1. ✅ Document decision (this file)
2. Create API specification document
3. Implement REST endpoints in server/
4. Add WebSocket handler for agent updates
5. Update client to use hybrid approach
6. Update GitHub issue #1 with decision

## Approval

**Decision:** Hybrid REST + WebSocket approach
**Status:** Recommended
**Blockers removed:** Server implementation can proceed
