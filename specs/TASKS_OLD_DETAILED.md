# Project Task List - Babocument

**Last Updated:** 2025-11-06 (REPRIORITIZED - All work tracked in GitHub)
**Current Phase:** Phase 1 Backend - 75% Complete
**GitHub Issues:** 18 open | 10 closed | All tasks now have issues

**🎯 CRITICAL PATH TO PHASE 1:** 9-12 hours remaining
1. Event Bus (Issue #19) - 3-4 hours ← **START HERE**
2. Agents (Issue #10) - 6-8 hours ← **THEN THIS**

**� Priority Tiers:**
- **P0 (Critical):** 2 tasks - BLOCKING Phase 1
- **P1 (High):** 4 tasks - Required for production
- **P2 (Medium):** 6 tasks - Quality improvements
- **P3 (Low):** 6 tasks - Future work

---

## 📋 All Tasks Organized by Priority

See **PRIORITY_ANALYSIS_2025-11-06.md** for complete dependency graph and rationale.

---

## P0 - CRITICAL (Must Complete for Phase 1)

### 1. Service Integration (Issue #15) - ✅ COMPLETED!
**Priority:** CRITICAL | **Status:** ✅ Complete | **Completed:** 2025-11-06

**Completed Tasks:**
- ✅ Connected `api/documents.py` search to `vector_db.search()` (already done)
- ✅ Connected `api/documents.py` list to `vector_db.get_all_papers()` (already done)
- ✅ File upload saves PDFs to disk + vector DB (already done)
- ✅ Connected document deletion to `vector_db.delete_paper()` (already done)
- ✅ LLM summarization on document retrieval (already done, fixed async issue)
- ✅ Implemented keyword search functionality
- ✅ Added timestamp tracking (created_at, updated_at) in vector DB
- ✅ Updated tests - all 92 tests passing!
- ✅ End-to-end test: Upload PDF → Store → Search (semantic & keyword) → Retrieve → Summarize

**GitHub Status:** Issue #15 should be marked COMPLETED and CLOSED

**Files Updated:**
- ✅ `server/app/api/documents.py` - Fixed LLM summarization, added timestamp parsing
- ✅ `server/app/services/vector_db.py` - Added keyword search, timestamp metadata
- ✅ `server/tests/test_api_documents.py` - Fixed async mock for LLM client

**Acceptance Criteria:**
- ✅ All API endpoints use real Vector DB and LLM services
- ✅ File upload saves PDFs and indexes them
- ✅ Search returns real results from ChromaDB (both semantic and keyword)
- ✅ Tests pass with real service integration (92/92 passing)
- ✅ Keyword search implemented with term frequency scoring
- ✅ Timestamps tracked in metadata

**Remaining Enhancements (Optional):**
- Text highlighting for search results (marked as TODO)
- Document section parsing (marked as TODO)

---

### 2. Event Bus Implementation - **DO THIS NEXT**
**Priority:** CRITICAL | **Time:** 3-4 hours | **Status:** Not started

**Tasks:**
- [ ] Create `server/app/utils/event_bus.py`
- [ ] Implement Redis pub/sub wrapper
- [ ] Add event types: `TaskStarted`, `TaskProgress`, `TaskComplete`, `TaskError`
- [ ] Integrate with Agent coordinator
- [ ] Add event publishing to API endpoints (background tasks)
- [ ] Create event subscriber for WebSocket broadcasting
- [ ] Write tests for event publishing/subscribing

**Files to Create:**
- `server/app/utils/event_bus.py` (new)
- `server/tests/test_event_bus.py` (new)

**Files to Update:**
- `server/app/agents/coordinator.py` (add event publishing)
- `server/app/config.py` (add Redis config)
- `server/requirements.txt` (ensure redis-py included)

**Acceptance Criteria:**
- ✅ Redis connection managed properly
- ✅ Events can be published and subscribed to
- ✅ Coordinator publishes agent lifecycle events
- ✅ Tests verify event delivery

---

### 3. Agent Implementation (Issue #10) - **DO THIS THIRD**
**Priority:** CRITICAL | **Time:** 6-8 hours | **Status:** Base classes only, agents not created

**PROBLEM:** Agents are referenced but don't exist! Only ResearchAgent skeleton created.

**Tasks:**
- [ ] **CREATE missing agent files** (currently don't exist):
  - [ ] `server/app/agents/analysis.py` - AnalysisAgent class
  - [ ] `server/app/agents/summary.py` - SummaryAgent class
  - [ ] `server/app/agents/recommendation.py` - RecommendationAgent class
- [ ] Complete Research Agent (`research.py` exists but skeleton only)
  - [ ] Implement vector DB search integration
  - [ ] Add query parsing with LLM
  - [ ] Implement result ranking
  - [ ] Add MCP integration (Phase 2 prep)
- [ ] Complete Analysis Agent  
  - [ ] Implement keyword extraction
  - [ ] Add trend analysis over time windows
  - [ ] Generate word clouds from corpus
- [ ] Complete Summary Agent
  - [ ] Integrate LLM summarization
  - [ ] Add configurable summary lengths
  - [ ] Extract key insights
- [ ] Complete Recommendation Agent
  - [ ] Find similar papers using vector DB
  - [ ] Suggest related research
  - [ ] Identify research gaps
- [ ] **FIX Coordinator** - Uncomment agent initialization (lines 43-46)
- [ ] **FIX main.py** - Pass vector_db and llm_client to coordinator
- [ ] Update Coordinator to route tasks to agents
- [ ] Write comprehensive tests for each agent

**Files to Create:**
- `server/app/agents/analysis.py` (new) ⚠️ MISSING
- `server/app/agents/summary.py` (new) ⚠️ MISSING
- `server/app/agents/recommendation.py` (new) ⚠️ MISSING
- `server/tests/test_agents.py` (new)

**Files to Update:**
- `server/app/agents/research.py` (complete implementation)
- `server/app/agents/coordinator.py` (uncomment lines 43-46, add routing logic)
- `server/app/main.py` (pass services to coordinator on startup)
- `server/tests/test_agents.py` (create)

**Acceptance Criteria:**
- ✅ All 4 agents fully functional
- ✅ Agents use Vector DB and LLM services
- ✅ Coordinator routes tasks correctly
- ✅ Events published for all agent operations
- ✅ >80% test coverage

---

## 🛠️ Supporting Tasks (Can Do in Parallel)

### 4. CI/CD Pipeline (Issue #18) - ⚠️ DUPLICATE ISSUE ON GITHUB
**Priority:** HIGH | **Time:** 2-3 hours | **Status:** Not started

**⚠️ ACTION REQUIRED:** Close GitHub issue #17 (duplicate of #18)

**Tasks:**
- [ ] Close duplicate issue #17 on GitHub
- [ ] Create `.github/workflows/server-ci.yml`
  - [ ] Run pytest on Python 3.13
  - [ ] Require 84% coverage
  - [ ] Run linting (black, flake8, mypy)
- [ ] Create `.github/workflows/client-ci.yml`
  - [ ] Run npm build on Node 18+
  - [ ] Run ESLint and TypeScript checks
  - [ ] Run client tests (when they exist)
- [ ] Add CI badges to README.md
- [ ] Test workflows on a branch before merging

**Acceptance Criteria:**
- ✅ All PRs must pass CI checks
- ✅ Coverage reports uploaded as artifacts
- ✅ Status badges visible in README

---

### 5. Database Layer for Metadata
**Priority:** MEDIUM | **Time:** 3-4 hours | **Status:** Not started

**Tasks:**
- [ ] Choose database: SQLite (dev) or PostgreSQL (prod)
- [ ] Create database schema
  - [ ] Documents table (metadata, paths, timestamps)
  - [ ] Workspaces table
  - [ ] Repository configurations
  - [ ] User preferences (future)
- [ ] Create SQLAlchemy models
- [ ] Add database initialization script
- [ ] Implement database migrations (Alembic)
- [ ] Update API endpoints to use database
- [ ] Write database tests

**Files to Create:**
- `server/app/models/database.py` (SQLAlchemy models)
- `server/app/utils/database.py` (DB connection)
- `server/migrations/` (Alembic migrations)
- `server/scripts/init_database.py`

**Acceptance Criteria:**
- ✅ Metadata persists across server restarts
- ✅ Migrations work smoothly
- ✅ Tests use SQLite in-memory DB

---

### 6. WebSocket Handler
**Priority:** MEDIUM | **Time:** 2-3 hours | **Status:** Not started

**Depends on:** Event Bus complete

**Tasks:**
- [ ] Create `server/app/api/websocket.py`
- [ ] Implement WebSocket endpoint `/ws/agents`
- [ ] Subscribe to Event Bus events
- [ ] Broadcast events to connected clients
- [ ] Add connection management (connect/disconnect)
- [ ] Add authentication/authorization
- [ ] Write WebSocket tests

**Files to Create:**
- `server/app/api/websocket.py`
- `server/tests/test_websocket.py`

**Files to Update:**
- `server/app/main.py` (remove TODO, register WebSocket)

**Acceptance Criteria:**
- ✅ Clients can connect via WebSocket
- ✅ Real-time task updates broadcast to clients
- ✅ Proper connection handling

---

### 7. Background Task Processing
**Priority:** MEDIUM | **Time:** 2-3 hours | **Status:** Not started

**Tasks:**
- [ ] Set up Celery worker configuration
- [ ] Create background tasks for:
  - [ ] PDF upload processing
  - [ ] Repository synchronization
  - [ ] Batch document indexing
- [ ] Add task status tracking
- [ ] Integrate with Event Bus
- [ ] Write task tests

**Files to Create:**
- `server/app/tasks/` (Celery tasks)
- `server/celery_worker.py`

**Acceptance Criteria:**
- ✅ Long-running tasks don't block API
- ✅ Task status queryable via API
- ✅ Events published for task progress

---

## 🆕 Newly Identified Tasks (Missing from Original Plan)

### 11. Authentication & Authorization Framework
**Priority:** MEDIUM | **Time:** 4-6 hours | **Status:** Not started

**Rationale:** Currently no auth - all endpoints open. Need basic framework for production.

**Tasks:**
- [ ] Choose auth strategy (JWT tokens, API keys, OAuth)
- [ ] Implement user model (if needed)
- [ ] Add authentication middleware to FastAPI
- [ ] Protect sensitive endpoints
- [ ] Add rate limiting
- [ ] Document auth flow in OpenAPI

**Files to Create:**
- `server/app/auth/` (new directory)
- `server/app/auth/models.py`
- `server/app/auth/middleware.py`
- `server/tests/test_auth.py`

---

### 12. API Documentation & Usage Guide
**Priority:** MEDIUM | **Time:** 2-3 hours | **Status:** OpenAPI exists, usage guide missing

**What's Done:**
- ✅ OpenAPI/Swagger at `/docs`
- ✅ Response models documented

**What's Needed:**
- [ ] Create `docs/API_USAGE_GUIDE.md`
- [ ] Add example curl commands for each endpoint
- [ ] Add Python client examples
- [ ] Add common workflows (upload → search → summarize)
- [ ] Add error handling examples
- [ ] Create Postman/Thunder Client collection

---

### 13. Error Handling Standardization
**Priority:** MEDIUM | **Time:** 2-3 hours | **Status:** Inconsistent patterns

**Current Issues:**
- Different error formats across endpoints
- Some TODOs return mock errors
- Inconsistent HTTP status codes
- Missing error details in some cases

**Tasks:**
- [ ] Create standard error response model
- [ ] Add error codes/types (not just messages)
- [ ] Ensure consistent HTTP status usage
- [ ] Add error logging with context
- [ ] Create error handling middleware
- [ ] Update tests to validate error formats

**Files to Update:**
- All API routers (`documents.py`, `repositories.py`, `stats.py`)
- Create `server/app/utils/errors.py` (new)

---

### 14. Performance Optimization Pass
**Priority:** LOW | **Time:** 4-6 hours | **Status:** Not started

**Areas to Optimize:**
- [ ] Add caching layer (Redis) for frequent queries
- [ ] Optimize vector DB queries (batch operations)
- [ ] Add pagination to all list endpoints
- [ ] Profile slow endpoints
- [ ] Add database connection pooling
- [ ] Implement lazy loading for large documents
- [ ] Add request timeout handling

---

### 15. Security Audit
**Priority:** MEDIUM | **Time:** 2-3 hours | **Status:** Not started

**Tasks:**
- [ ] Add input sanitization for all endpoints
- [ ] Validate file uploads (size limits, type checking)
- [ ] Add CORS configuration
- [ ] Implement CSP headers
- [ ] Add rate limiting per IP/user
- [ ] Sanitize error messages (no stack traces in production)
- [ ] Add request logging for security events
- [ ] Review dependencies for vulnerabilities

---

### 16. Monitoring & Observability
**Priority:** LOW | **Time:** 3-4 hours | **Status:** Basic logging exists

**What's Done:**
- ✅ Structlog for structured logging

**What's Needed:**
- [ ] Add Prometheus metrics endpoint
- [ ] Track request latency by endpoint
- [ ] Monitor vector DB query performance
- [ ] Track LLM API call durations
- [ ] Add system resource monitoring
- [ ] Create Grafana dashboard configs
- [ ] Set up alerting rules

---

## 🧹 Code Quality & Maintenance

### 8. Resolve All TODO Comments
**Priority:** MEDIUM | **Time:** 2-3 hours

**19 TODOs found in code** (down from 21):
- `server/app/main.py` - 3 TODOs (resource init, cleanup, health checks)
- `server/app/api/stats.py` - 5 TODOs (task tracking, agent stats)
- `server/app/api/repositories.py` - 5 TODOs (MCP integration Phase 2)
- `server/app/api/documents.py` - 2 TODOs (text highlighting, section parsing)
- `server/app/agents/research.py` - 1 TODO (implement search logic)
- `server/app/agents/coordinator.py` - 1 TODO (initialize agents)
- `server/app/services/vector_db.py` - 1 TODO (optimize large collections)
- `server/app/utils/pdf_processing.py` - 1 TODO (smarter parsing)

**Action Plan:**
- Convert each TODO to a GitHub issue or implement inline
- Tag with appropriate priority
- Add to this task list

---

### 9. Documentation Cleanup
**Priority:** LOW | **Time:** 1-2 hours

**Remove/Consolidate:**
- [ ] Archive SESSION_*.md files to `docs/sessions/` or create CHANGELOG.md
- [ ] Delete or merge redundant docs:
  - [ ] `BABYLON_CLIENT_STRUCTURE.md` → `client/README.md`
  - [ ] `BABYLON_QUICK_REFERENCE.md` → `client/README.md`
  - [ ] `EXPLORATION_SUMMARY.md` → Delete (outdated)
  - [ ] `ASSET_DOCUMENTATION_INDEX.md` → Delete (covered in HANDOFF.md)
  - [ ] `PROJECT_ASSET_STRUCTURE.md` → `docs/BLENDER_WORKFLOW.md`
  - [ ] `BLENDER_INTEGRATION_PLAN.md` → `docs/BLENDER_WORKFLOW.md`
- [ ] Update all references in remaining docs
- [ ] Simplify root directory (keep only: README, HANDOFF, ISSUES, LICENSE)

**Result:** Cleaner repository, less confusion

---

### 10. Linting & Code Formatting
**Priority:** LOW | **Time:** 1 hour

**Tasks:**
- [ ] Run `black` formatter on all Python code
- [ ] Run `flake8` and fix issues
- [ ] Run `mypy` for type checking
- [ ] Add pre-commit hooks
- [ ] Update CI to enforce formatting

---

## 📋 Future Phases (Not Blocking Phase 1)

### Phase 2: MCP Integration (After Phase 1 Complete)
**Priority:** NEXT PHASE | **Time:** 1-2 weeks

**Prerequisite:** Phase 1 complete (agents working)

**Tasks:**
- [ ] Install BioMCP server
- [ ] Install arXiv MCP server  
- [ ] Install bioRxiv/medRxiv MCP servers
- [ ] Integrate MCP clients with Research Agent
- [ ] Add repository management endpoints
- [ ] Test multi-source search
- [ ] Add result deduplication

---

### Issue #6: Plotly Integration Decision
**Priority:** NEXT PHASE | **Type:** Decision

**Tasks:**
- [ ] Test canvas texture mapping approach
- [ ] Test HTML overlay approach
- [ ] Benchmark performance
- [ ] Choose strategy
- [ ] Document decision

---

### Issue #7: Blender Asset Pipeline
**Priority:** NEXT PHASE | **Type:** Setup

**Tasks:**
- [ ] Set up Blender directories
- [ ] Document export workflow
- [ ] Create first asset (Librarian character)
- [ ] Test import in BabylonJS

---

### Issue #14: Select Specific LLM Models
**Priority:** LOW | **Type:** Decision

**Tasks:**
- [ ] Benchmark different models for each agent task
- [ ] Compare speed vs quality
- [ ] Document findings
- [ ] Update configuration

---

## 📊 Summary

**Critical Path (Phase 1 Completion):** ~13-17 hours
1. Service Integration (4-5h)
2. Event Bus (3-4h)
3. Agent Implementation (6-8h)

**Supporting Work:** ~10-14 hours
4. CI/CD (2-3h)
5. Database Layer (3-4h)
6. WebSocket (2-3h)
7. Background Tasks (2-3h)

**Cleanups:** ~4-6 hours
8. TODO Resolution (2-3h)
9. Documentation (1-2h)
10. Linting (1h)

**Total Phase 1 Remaining:** ~27-37 hours of focused work

---

## ✅ Completed (For Reference)

- ✅ Phase 0 Decisions (6/7) - Issues #1-5, #12
- ✅ Python environment setup
- ✅ FastAPI application structure
- ✅ Vector DB service (ChromaDB)
- ✅ LLM Client service (Ollama/LiteLLM)
- ✅ REST API scaffolding (17 endpoints)
- ✅ Test suite (60 tests, 84% coverage)
- ✅ Agent base classes
- ✅ Project documentation

---

**Next Session:** Start with Service Integration (Issue #15) - Critical path priority #1
