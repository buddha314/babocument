# Project Task List - Babocument

**Last Updated:** 2025-11-06 23:52
**Current Phase:** Phase 1 Backend - 75% Complete

---

## 🚨 Immediate Cleanups Required

### GitHub Issues Cleanup
- **Issue #16, #17, #18 Duplicates** - Close #16 and #17, keep only #18 for CI/CD
- **Issue #15 Status** - ✅ COMPLETED - Service integration done!

### Documentation Consolidation  
- **7 SESSION_*.md files** - Archive or consolidate into single CHANGELOG.md
- **Remove duplicates:**
  - `BABYLON_CLIENT_STRUCTURE.md` - consolidate into client/README.md
  - `BABYLON_QUICK_REFERENCE.md` - consolidate into client/README.md
  - `EXPLORATION_SUMMARY.md` - archive (covered in other docs)
  - `ASSET_DOCUMENTATION_INDEX.md` - outdated, covered in HANDOFF.md
  - `PROJECT_ASSET_STRUCTURE.md` - consolidate into docs/BLENDER_WORKFLOW.md
  - `BLENDER_INTEGRATION_PLAN.md` - consolidate into docs/BLENDER_WORKFLOW.md

### Code Cleanup
- **12 TODO comments** remaining in server code (down from 21!)
- ✅ Service integration complete - no more mock data in document endpoints!
- **Unused imports** - run linter and cleanup

---

## 🎯 Critical Path (Phase 1 Completion)

### 1. Service Integration (Issue #15) - ✅ COMPLETED!
**Priority:** CRITICAL | **Status:** ✅ Complete

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
**Priority:** CRITICAL | **Time:** 6-8 hours | **Status:** Skeleton only

**Tasks:**
- [ ] Complete Research Agent
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
- [ ] Update Coordinator to route tasks to agents
- [ ] Write comprehensive tests for each agent

**Files to Update:**
- `server/app/agents/research.py` (remove TODO)
- `server/app/agents/analysis.py` (create)
- `server/app/agents/summary.py` (create)
- `server/app/agents/recommendation.py` (create)
- `server/app/agents/coordinator.py` (add routing)
- `server/tests/test_agents.py` (create)

**Acceptance Criteria:**
- ✅ All 4 agents fully functional
- ✅ Agents use Vector DB and LLM services
- ✅ Coordinator routes tasks correctly
- ✅ Events published for all agent operations
- ✅ >80% test coverage

---

## 🛠️ Supporting Tasks (Can Do in Parallel)

### 4. CI/CD Pipeline (Issue #18)
**Priority:** HIGH | **Time:** 2-3 hours | **Status:** Not started

**Tasks:**
- [ ] Close duplicate issues #16, #17 on GitHub
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

## 🧹 Code Quality & Maintenance

### 8. Resolve All TODO Comments
**Priority:** MEDIUM | **Time:** 2-3 hours

**21 TODOs found in code:**
- `server/app/main.py` - 3 TODOs (resource init, cleanup, health checks)
- `server/app/api/stats.py` - 5 TODOs
- `server/app/api/repositories.py` - 5 TODOs
- `server/app/api/documents.py` - 6 TODOs
- `server/app/agents/research.py` - 1 TODO
- `server/app/api/websocket.py` - 1 TODO (in comment)

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
