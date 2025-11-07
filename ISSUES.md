# GitHub Issues Index

**Repository:** https://github.com/buddha314/babocument/issues

**Last Updated:** 2025-11-06 (Event Bus Complete)

**Total Issues:** 8 open on GitHub (need to close completed ones)

---

## 🚨 Immediate Actions Required

**GitHub Cleanup:**
1. ✅ Close issue #9 - Vector DB initialization COMPLETED
2. ✅ Close issue #15 - Service Integration COMPLETED  
3. ✅ Close issue #17 - Duplicate of #18 (CI/CD)
4. ✅ Close issue #19 - Event Bus COMPLETED
5. ✅ Create new issue for Database Layer
6. ✅ Create new issue for WebSocket Handler
7. ⚠️ Update issue #10 description - Note agent files are missing

**See [specs/TASKS.md](specs/TASKS.md) for complete task breakdown**

---

## 📊 Quick Summary

**Status:**
- **Open:** 17 issues (after closing #19)
- **Closed:** 11 issues
- **Phase 1:** 85% Complete

**Priority Breakdown:**
- **P0 (Critical):** 1 issue - Issue #10 (Agents)
- **P1 (High):** 4 issues - Required for production
- **P2 (Medium):** 6 issues - Quality improvements
- **P3 (Low):** 6 issues - Future work

**Critical Path:**  
~~Issue #19 (Event Bus)~~ ✅ → Issue #10 (Agents) → Phase 1 Complete

Critical architectural decisions that must be made before implementation.

---

### [Issue #1: Choose client-server communication protocol](https://github.com/buddha314/babocument/issues/1)

## P0 - CRITICAL PRIORITY**Status:** ✅ DECIDED | **Priority:** High | **Type:** Decision



### #19: Event Bus Implementation ⭐ **DO FIRST****Decision Date:** 2025-11-06

**Status:** Open | **Priority:** P0 | **Time:** 3-4 hours

Choose between WebSockets (real-time) vs REST API with async (simpler)

Implement Redis pub/sub for agent coordination and real-time updates.

**Impact:** Backend architecture, real-time capabilities, agent communication

**Why Critical:** Blocks agent initialization and WebSocket implementation.**Blocking:** Phase 1 server implementation



**Created:** 2025-11-06  ---

**Link:** https://github.com/buddha314/babocument/issues/19

### [Issue #2: Design multi-agent architecture](https://github.com/buddha314/babocument/issues/2)

---**Status:** ✅ DECIDED | **Priority:** High | **Type:** Decision



### #10: Phase 1 - Set up FastAgent backend ⭐ **DO SECOND****Decision Date:** 2025-11-06

**Status:** Open (75% complete) | **Priority:** P0 | **Time:** 6-8 hours

Design FastAgent multi-agent system for coordinating Research, Analysis, Summary, and Recommendation agents.

Complete agent implementation - 3 of 4 agent files missing.

**Decisions needed:**

**Why Critical:** Core intelligence layer. Phase 1 can't complete without this.- Agent roles and responsibilities

- Communication patterns

**Critical Finding:** analysis.py, summary.py, recommendation.py don't exist - must create.- State management approach



**Link:** https://github.com/buddha314/babocument/issues/10**Impact:** Agent intelligence, system complexity, scalability

**Blocking:** Phase 1 server implementation

---

---

## P1 - HIGH PRIORITY (Production Required)

### [Issue #3: Choose local LLM hosting solution](https://github.com/buddha314/babocument/issues/3)

### #27: Security Audit & Hardening**Status:** ✅ DECIDED | **Priority:** High | **Type:** Decision

**Status:** Open | **Priority:** P1 | **Time:** 2-3 hours

**Decision Date:** 2025-11-06

Security hardening before production deployment.

Select local LLM hosting: Ollama, HuggingFace Transformers, or LangGraph

**Link:** https://github.com/buddha314/babocument/issues/27

**Options:**

---- **Ollama:** Easy setup, local inference, privacy-focused

- **HuggingFace:** Model hub access, research flexibility

### #23: Authentication & Authorization Framework- **LangGraph:** Agentic workflows, state management

**Status:** Open | **Priority:** P1 | **Time:** 4-6 hours

**Impact:** Agent capabilities, deployment complexity, hosting costs

Implement auth - currently all endpoints are open.

---

**Link:** https://github.com/buddha314/babocument/issues/23

### [Issue #4: Vector database selection](https://github.com/buddha314/babocument/issues/4)

---**Status:** ✅ DECIDED | **Priority:** High | **Type:** Decision



### #18: Implement CI/CD pipeline**Decision Date:** 2025-11-06

**Status:** Open | **Priority:** P1 | **Time:** 2-3 hours

**Decision:** Use **ChromaDB** with **Sentence Transformers** (all-MiniLM-L6-v2) for vector storage

GitHub Actions for automated testing.

**Rationale:**

**Note:** Issues #16, #17 closed as duplicates.- ✅ Simplest setup (pip install, no separate server)

- ✅ Python-native (perfect for FastAgent backend)

**Link:** https://github.com/buddha314/babocument/issues/18- ✅ Configurable local storage paths

- ✅ Built-in embedding support

---- ✅ Free and open source

- ✅ Sufficient performance for 100k+ documents

### #20: Database Layer for Metadata- ✅ Easy migration path to Weaviate/Qdrant if needed

**Status:** Open | **Priority:** P1 | **Time:** 3-4 hours

**Embedding Strategy:**

SQLAlchemy models for persistent metadata.- **Model:** all-MiniLM-L6-v2 (384 dimensions)

- **Speed:** ~3000 sentences/sec on CPU

**Link:** https://github.com/buddha314/babocument/issues/20- **Quality:** Good for general scientific text

- **Cost:** $0 (local inference)

---

**Storage Structure:**

## P2 - MEDIUM PRIORITY (Quality)```

server/data/chroma/

### #21: WebSocket Handler for Real-time Updates├── chroma.sqlite3

**Status:** Open | **Priority:** P2 | **Time:** 2-3 hours  └── embeddings/

**Depends on:** #19```



**Link:** https://github.com/buddha314/babocument/issues/21**Documentation:** 

- [specs/VECTOR_DATABASE_DECISION.md](specs/VECTOR_DATABASE_DECISION.md) - Decision rationale and implementation

---- [specs/VECTOR_DATABASE_SPEC.md](specs/VECTOR_DATABASE_SPEC.md) - Comprehensive analysis



### #22: Background Task Processing with Celery**Next Steps:** 

**Status:** Open | **Priority:** P2 | **Time:** 2-3 hours  - Phase 1: Install ChromaDB and implement VectorDatabase wrapper class

**Depends on:** #19- Phase 2: Create initialization script for data/papers corpus

- Phase 3: Integrate with Research Agent for semantic search

**Link:** https://github.com/buddha314/babocument/issues/22

**Unblocks:**

---- ✅ Issue #9 - Initialize vector database with local papers

- ✅ Phase 1 - Backend setup can proceed

### #25: Error Handling Standardization- ✅ Phase 2 - MCP integration can use vector DB for caching

**Status:** Open | **Priority:** P2 | **Time:** 2-3 hours- ✅ Issue #8 - Keyword trend analysis has data source



**Link:** https://github.com/buddha314/babocument/issues/25---



---### [Issue #5: MCP integration strategy for document repositories](https://github.com/buddha314/babocument/issues/5)

**Status:** ✅ DECIDED | **Priority:** High | **Type:** Decision

### #28: Resolve All TODO Comments in Codebase

**Status:** Open | **Priority:** P2 | **Time:** 2-3 hours**Decision Date:** 2025-11-06



Clean up 19 TODO comments.**Decision:** Hybrid approach using community MCP servers with custom extensions



**Link:** https://github.com/buddha314/babocument/issues/28**Selected Community Servers:**

- **BioMCP** - Primary biomedical source (PubMed + ClinicalTrials.gov + MyVariant.info)

---- **arXiv API MCP** - Physics, CS, biology papers with LaTeX support

- **bioRxiv/medRxiv MCP** - Biology and medicine preprints

### #24: API Documentation & Usage Guide

**Status:** Open | **Priority:** P2 | **Time:** 2-3 hours**Rationale:**

- ✅ Leverage existing, maintained community servers

**Link:** https://github.com/buddha314/babocument/issues/24- ✅ BioMCP purpose-built for biomedical research (perfect match)

- ✅ Faster implementation (weeks vs months)

---- ✅ Focus development on Babocument-specific features

- ✅ Build custom servers only when needed

### #14: Decision: Select optimal local LLMs

**Status:** Open | **Priority:** P2 | **Time:** Research**Documentation:** [specs/MCP_INTEGRATION_DECISION.md](specs/MCP_INTEGRATION_DECISION.md) (6 KB)



**Link:** https://github.com/buddha314/babocument/issues/14**Implementation Plan:**

- **Week 1-2:** Install and test 3 community MCP servers

---- **Week 3-4:** Build Research Agent with unified interface

- **Week 5-6:** Integrate vector database and caching

## P3 - LOW PRIORITY (Future)- **Week 7-8:** Create API endpoints



### #29: Code Linting & Formatting Setup**Impact:** Accelerates Phase 2 (data integration), enables Phase 5 (intelligence features)

**Status:** Open | **Priority:** P3 | **Time:** 1 hour

**Next Steps:** Begin Phase 1 MCP server installation and testing

**Link:** https://github.com/buddha314/babocument/issues/29

---

---

### [Issue #6: Plotly.js integration strategy for 3D visualization](https://github.com/buddha314/babocument/issues/6)

### #26: Documentation Cleanup & Consolidation**Status:** 🟡 Open | **Priority:** Medium | **Type:** Decision

**Status:** Open | **Priority:** P3 | **Time:** 1-2 hours

Determine how to integrate Plotly.js scientific visualizations into BabylonJS 3D scenes

**Link:** https://github.com/buddha314/babocument/issues/26

**Strategies:**

---- **A:** Canvas texture mapping (best for VR)

- **B:** HTML overlay (best for desktop)

### #6: Decision: Plotly.js integration strategy- **C:** Native BabylonJS conversion (maximum performance)

**Status:** Open | **Priority:** P3 | **Type:** Decision (Phase 3)- **Recommended:** Hybrid (auto-detect mode)



**Link:** https://github.com/buddha314/babocument/issues/6**Documentation:** [docs/PLOTLY_BABYLONJS_INTEGRATION.md](docs/PLOTLY_BABYLONJS_INTEGRATION.md) (16 KB)



---**Impact:** Visualization capabilities, performance, UX



### #7: Setup: Blender asset pipeline---

**Status:** Open | **Priority:** P3 | **Type:** Setup (Phase 3)

### [Issue #7: Setup Blender asset pipeline](https://github.com/buddha314/babocument/issues/7)

**Link:** https://github.com/buddha314/babocument/issues/7**Status:** 🟡 Open | **Priority:** Medium | **Type:** Setup



---Establish Blender → GLTF 2.0 → GLB export workflow for 3D assets



### #8: Implement keyword trend line graphs**Tasks:**

**Status:** Open | **Priority:** P3 | **Type:** Feature (Phase 5)  - Create directory structure for .blend sources and .glb exports

**Depends on:** #10- Document export settings

- Update .gitignore

**Link:** https://github.com/buddha314/babocument/issues/8- Create contributor guidelines



---**Assets needed:**

- Phase 3: File Room environment

### #11: Phase 3: Implement data visualization UI- Phase 4: Librarian character (rigged, animated)

**Status:** Open | **Priority:** P3 | **Type:** Epic (Phase 3)- Phase 7: Lab equipment models



**Link:** https://github.com/buddha314/babocument/issues/11**Documentation:**

- [BLENDER_INTEGRATION_PLAN.md](BLENDER_INTEGRATION_PLAN.md)

---- [docs/BLENDER_WORKFLOW.md](docs/BLENDER_WORKFLOW.md) (7 KB)



## ✅ CLOSED ISSUES---



### #17: CI/CD pipeline (duplicate)## Feature Implementation Issues

**Status:** Closed | **Closed:** 2025-11-06  

**Reason:** Duplicate of #18### [Issue #8: Implement keyword trend line graphs](https://github.com/buddha314/babocument/issues/8)

**Status:** 🟡 Open | **Priority:** High | **Type:** Feature

---

Enable Beabadoo to visualize keyword frequency trends over time across research corpus

### #16: CI/CD pipeline (duplicate)

**Status:** Closed | **Closed:** 2025-11-06  **User Story:**

**Reason:** Duplicate of #18> As Beabadoo, I want to see how frequently specific keywords appear in research papers over time, so I can understand the evolution and popularity of research topics in biomanufacturing.



---**Features:**

- Compare up to 10 keywords simultaneously

### #15: Implement REST API endpoints- Interactive hover, zoom, pan

**Status:** Closed | **Completed:** 2025-11-06- Export as PNG/SVG and CSV/JSON

- Desktop (HTML overlay) and VR (3D texture) modes

Service integration complete. 17 endpoints, 92 tests, 84% coverage.

**Phases:** 5 (Backend), 3 & 6 (Frontend)

---

**Dependencies:** [#6](#issue-6-plotlyjs-integration-strategy-for-3d-visualization), [#4](#issue-4-vector-database-selection)

### #12: Develop devcontainer

**Status:** Closed | **Completed:** 2025-11-06**Documentation:** [specs/VISUALIZATION_REQUIREMENTS.md](specs/VISUALIZATION_REQUIREMENTS.md)



Launch scripts created.---



---### [Issue #9: Initialize vector database with local papers](https://github.com/buddha314/babocument/issues/9)

**Status:** ✅ COMPLETED | **Priority:** High | **Type:** Implementation

### #9: Initialize vector database**Completed:** 2025-11-06

**Status:** Closed | **Completed:** 2025-11-06

**✅ ACTION:** Close this issue on GitHub - work is complete

4 papers indexed, semantic search working.

Create initialization script to populate vector database from data/papers directory

---

**Completed:**

### #5: Decision: MCP integration strategy- ✅ Parse PDFs from `data/papers/` (4 papers indexed)

**Status:** Closed | **Decided:** 2025-11-06- ✅ Extract full text and metadata

- ✅ Generate embeddings using Sentence Transformers (all-MiniLM-L6-v2)

Use community MCP servers (BioMCP, arXiv, bioRxiv).- ✅ Configurable storage paths (server/data/chroma/)

- ✅ Semantic search functionality implemented and tested

---

**Deliverables:**

### #4: Decision: Vector database selection- `server/scripts/init_vector_db.py` - Initialization script

**Status:** Closed | **Decided:** 2025-11-06- `server/scripts/test_vector_search.py` - Search testing script

- `server/app/services/vector_db.py` - ChromaDB service wrapper

ChromaDB with Sentence Transformers.- 4 papers from data/papers/ successfully indexed



---**Phases:** 1 (Backend - Complete)



### #3: Decision: LLM hosting solution**Dependencies:** [#4](#issue-4-vector-database-selection) ✅

**Status:** Closed | **Decided:** 2025-11-06

**Documentation:** [specs/VECTOR_DATABASE_SPEC.md](specs/VECTOR_DATABASE_SPEC.md)

Ollama + LiteLLM.

---

---

### [Issue #12: Develop devcontainer for server application](https://github.com/buddha314/babocument/issues/12)

### #2: Decision: Multi-agent architecture**Status:** ✅ Completed | **Priority:** High | **Type:** DevOps

**Status:** Closed | **Decided:** 2025-11-06**Completed:** 2025-11-06



Event-driven coordinator with specialized agents.Create development container configuration for FastAgent server with all Python dependencies and MCP server integrations.



---**Requirements:**

- Python 3.11+ environment

### #1: Decision: Client-server communication- FastAgent dependencies

**Status:** Closed | **Decided:** 2025-11-06- ChromaDB and vector database tools

- MCP server integration support

REST + WebSocket hybrid.- Development tools and extensions



---**Deliverables:**

- `.devcontainer/devcontainer.json` - Container configuration

## 📈 Progress Tracking- `server/requirements.txt` - Python dependencies

- Documentation in README.md

**Phase 1 Backend:**

- Current: 75% complete**Benefits:**

- After #19 (Event Bus): ~85%- Consistent development environment

- After #10 (Agents): 100% ✅- Simplified onboarding for contributors

- Isolated dependency management

**Production Readiness:**- Works with VS Code Remote Containers

- Phase 1: 75% → 100% (9-12 hours)

- P1 Tasks: 11-16 hours**Phases:** 0 (DevOps), applies to Phase 1+

- **Total:** 20-28 hours to production-ready

**Dependencies:** None (can implement immediately)

---

---

## 🎯 Recommended Work Order

### [Issue #14: Select optimal local LLMs for research paper analysis](https://github.com/buddha314/babocument/issues/14)

**Week 1: Complete Phase 1****Status:** 🟡 Open | **Priority:** High | **Type:** Decision

1. Issue #19: Event Bus (3-4 hours)

2. Issue #10: Agents (6-8 hours)Evaluate and select specific local LLM models for different agent tasks in the multi-agent system.



**Week 2: Production Readiness (P1)****Agent-Specific Requirements:**

3. Issue #27: Security Audit (2-3 hours)- **Research Agent:** Query understanding, semantic search

4. Issue #23: Authentication (4-6 hours)- **Analysis Agent:** Trend analysis, pattern detection

5. Issue #18: CI/CD (2-3 hours)- **Summary Agent:** Document summarization, key insight extraction

6. Issue #20: Database Layer (3-4 hours)- **Recommendation Agent:** Related paper suggestions, gap identification



**Week 3: Quality & Enhancement (P2)****Evaluation Criteria:**

7. Issues #21, #22, #25, #28, #24, #14- Model size vs performance trade-offs

- Inference speed for real-time responses

**Ongoing: (P3)**- Context window size for long documents

- Low priority cleanup and future features- Fine-tuning potential for scientific domain

- Local hosting feasibility

---

**Candidate Models:**

## 🔗 Quick Links- Llama 3.1 (8B, 70B variants)

- Mistral 7B / Mixtral 8x7B

**View All Issues:** https://github.com/buddha314/babocument/issues  - Qwen 2.5 (specialized models)

**Create New Issue:** https://github.com/buddha314/babocument/issues/new  - Domain-specific models (BioGPT, SciBERT embeddings)

**Priority Analysis:** PRIORITY_ANALYSIS_2025-11-06.md  

**Task List:** specs/TASKS.md**Impact:** Agent intelligence quality, response speed, resource requirements



---**Dependencies:** [#3](#issue-3-choose-local-llm-hosting-solution) (hosting solution)



## 📝 Notes---



- All outstanding work now tracked in GitHub### [Issue #15: Implement REST API endpoints for document and repository management](https://github.com/buddha314/babocument/issues/15)

- Clear dependency chain established**Status:** ✅ COMPLETED | **Priority:** High | **Type:** Feature

- Priority tiers align with project goals**Completed:** 2025-11-06

- Next action: Start Issue #19

**✅ ACTION:** Close this issue on GitHub - work is complete

**Last Review:** 2025-11-06

**What Was Completed:**
- ✅ 17 REST endpoints defined with Pydantic models
- ✅ OpenAPI/Swagger documentation
- ✅ 92 tests with 84% coverage
- ✅ Error handling and validation
- ✅ Connected to Vector DB service (semantic + keyword search)
- ✅ Connected to LLM Client service (summarization)
- ✅ File upload with PDF storage and indexing
- ✅ Timestamp tracking (created_at, updated_at)

**Testing:**
- All 92 tests passing
- End-to-end workflow validated

**Documentation:** See HANDOFF_2025-11-06_SERVICE_INTEGRATION.md

**Note:** Original issue description said "scaffolding only" but implementation is now complete with real service integration.

---

### [Issue #18: Implement CI/CD pipeline with GitHub Actions](https://github.com/buddha314/babocument/issues/18)
**Status:** 🟡 Open | **Priority:** Medium | **Type:** Enhancement

**⚠️ NOTE:** Issue #17 is a duplicate - close #17, keep only #18

**Summary:**
Implement automated CI/CD pipeline using GitHub Actions for both server and client.

**Server Pipeline:**
- Run pytest with 84% coverage requirement
- Python 3.13 environment
- Linting (flake8/black/mypy)

**Client Pipeline:**
- Next.js build validation
- Node.js 18+ environment
- ESLint and TypeScript checking

**Why Not Critical Path:** Doesn't block other work, helps with quality but not required for functionality

**Deliverables:**
- `.github/workflows/server-ci.yml`
- `.github/workflows/client-ci.yml`
- PR status checks

**Estimated Effort:** 2-3 hours

---

### [Issue #15: Implement REST API endpoints for document and repository management](https://github.com/buddha314/babocument/issues/15)
**Status:** ✅ COMPLETED | **Priority:** High | **Type:** Feature | **ARCHIVED - See above**

**Problem:**
Currently, the server has only basic health check endpoints. Document management functions are either not implemented or not exposed via API, making it impossible to:
- List available documents in the corpus
- Retrieve document metadata and content
- Upload new documents to the system
- Search across documents
- Manage repository connections
- Track document processing status

**Required API Endpoints:**

**Document Operations:**
- `GET /api/v1/documents` - List all documents with pagination
- `GET /api/v1/documents/{id}` - Get document details and metadata
- `GET /api/v1/documents/{id}/content` - Get full document content
- `POST /api/v1/documents` - Upload new document(s)
- `DELETE /api/v1/documents/{id}` - Remove document from system
- `GET /api/v1/documents/search` - Search documents by keyword/semantic query

**Repository Operations:**
- `GET /api/v1/repositories` - List connected repositories (MCP servers)
- `GET /api/v1/repositories/{id}/status` - Check repository connection status
- `POST /api/v1/repositories/sync` - Trigger repository synchronization
- `GET /api/v1/repositories/{id}/documents` - List documents from specific repository

**Statistics & Status:**
- `GET /api/v1/stats` - System statistics (doc count, embeddings, storage)
- `GET /api/v1/status/processing` - Check document processing queue status

**Acceptance Criteria:**
- [ ] All endpoints documented in OpenAPI/Swagger (`/docs`)
- [ ] Proper error handling with meaningful HTTP status codes
- [ ] Request validation using Pydantic models
- [ ] Pagination support for list endpoints (limit/offset or cursor)
- [ ] Authentication/authorization framework (even if initially permissive)
- [ ] Unit tests for each endpoint
- [ ] Integration tests for end-to-end workflows
- [ ] Rate limiting considerations documented

**Technical Implementation:**
- FastAPI router structure in `server/app/api/`
- Separate routers for documents, repositories, stats
- Service layer for business logic
- Database/VectorDB integration for data access
- Background tasks for async operations (upload processing)

**Dependencies:**
- [#4](#issue-4-vector-database-selection) (ChromaDB integration)
- [#9](#issue-9-initialize-vector-database-with-local-papers) (Vector DB populated)
- [#10](#issue-10-phase-1---set-up-fastagent-backend) (Backend framework)

**Phases:** Phase 1 (Backend), Phase 2 (MCP Integration)

**Priority Rationale:** 
High priority because this blocks agent functionality. Agents need these APIs to access and manipulate documents. Without this, the multi-agent system cannot perform its core functions.

**Documentation Requirements:**
- OpenAPI schema auto-generated from FastAPI
- README section with example API calls
- Postman/Thunder Client collection for testing

---

## Epic Issues (Multi-task)

### [Issue #10: Phase 1 - Set up FastAgent backend](https://github.com/buddha314/babocument/issues/10)
**Status:** 🟡 Open (In Progress - 75% complete) | **Priority:** High | **Type:** Epic
**Timeline:** 1-2 weeks

**⚠️ CRITICAL FINDING:** Agent files are missing!
- AnalysisAgent (`analysis.py`) - NOT CREATED
- SummaryAgent (`summary.py`) - NOT CREATED  
- RecommendationAgent (`recommendation.py`) - NOT CREATED
- ResearchAgent exists but skeleton only
- Coordinator has agents commented out (can't initialize without files)

Initialize Python backend with FastAgent framework and multi-agent coordination

**Prerequisites:** Issues #1, #2, #3, #4 (all Phase 0 decisions) ✅

**Major tasks:**
- ✅ Initialize Python project structure
- ✅ Set up FastAgent framework (base classes done)
- ⚠️ Implement agent coordinator/orchestrator (commented out, needs fixing)
- ⚠️ Create agent classes (3 of 4 missing!)
- ✅ Define API endpoints (17 endpoints complete)
- ✅ Configure vector database integration
- ✅ Set up logging and monitoring

**Completion:** ~75% (APIs done, agents not created)

**Documentation:** [specs/TASKS.md](specs/TASKS.md) (Phase 1, lines 57-76)

---

### [Issue #11: Phase 3 - Implement data visualization UI](https://github.com/buddha314/babocument/issues/11)
**Status:** 🟡 Open | **Priority:** Medium | **Type:** Epic
**Timeline:** 2-3 weeks (part of Phase 3)

Build immersive data visualization UI with Plotly.js in BabylonJS

**Prerequisites:** [#6](#issue-6-plotlyjs-integration-strategy-for-3d-visualization), Basic server API

**Components:**
- Word cloud display
- Keyword trend line graphs (2D and 3D)
- 3D scatter plots (document clustering)
- 3D surface plots (research landscape)
- Heatmaps and correlation matrices
- Interactive chart controls

**Rendering strategies:**
- HTML overlay for desktop
- Canvas texture mapping for VR
- Auto-detect mode switching

**Documentation:**
- [docs/PLOTLY_BABYLONJS_INTEGRATION.md](docs/PLOTLY_BABYLONJS_INTEGRATION.md)
- [specs/VISUALIZATION_REQUIREMENTS.md](specs/VISUALIZATION_REQUIREMENTS.md)

---

## Issue Status Summary

**Total Issues:** 8 open on GitHub (after cleanup: 5 open, 3 to close)
**Actual Unique Issues:** After removing duplicates and closing completed

**To Close on GitHub:**
- ✅ Issue #9 - Vector DB initialization COMPLETED
- ✅ Issue #15 - Service Integration COMPLETED
- ✅ Issue #17 - Duplicate of #18 (CI/CD)

**Completed:** 9 total (Issues #1, #2, #3, #4, #5, #9, #12, #15)
**In Progress:** 2 (Issues #10 - Agents at 75%, #6 - Plotly decision pending)
**Open:** 5 (Issues #6, #7, #8, #11, #14, #18)

**Missing Issues (Need to Create):**
- 🆕 Event Bus implementation (critical path #2)
- 🆕 Database Layer for metadata
- 🆕 WebSocket Handler
- 🆕 Authentication & Authorization
- 🆕 API Documentation & Usage Guide

**By Type:**
- 🔷 Decisions: 7 total (5 completed: #1-5, 2 open: #6, #14)
- 🔶 Setup: 1 (Issue #7 - open)
- ⚙️ Features: 4 (Issues #9, #15 completed; Issue #8 open)
- 📦 Epics: 2 (Issue #10 at 75%, Issue #11 - both need backend first)
- 🛠️ DevOps: 2 (Issue #12 completed, Issue #18 open with duplicate #17)

**By Priority:**
- 🔴 **Critical Path:** 2 remaining (Event Bus creation needed, Agent Implementation #10)
- 🟡 **High (Supporting):** 2 (Issue #18 CI/CD, Database Layer needed)
- 🟢 **Medium:** 5 (Issues #6, #7, #8, #11, #14)

**By Phase:**
- Phase 0 (Planning): 7 decision issues (5 completed, 2 open: #6, #14)
- Phase 1 (Backend): 3 (Issue #10 epic in progress, #15 scaffolded, Event Bus pending)
- Phase 2 (Data): 0 open (MCP integration ready after Phase 1)
- Phase 3 (Frontend): 2 (Issue #11 epic, #8 feature - both need backend first)

---

---

## 🆕 New Issues to Create on GitHub

### Issue: Event Bus Implementation (Critical Path #2)
**Priority:** CRITICAL | **Type:** Feature | **Timeline:** 3-4 hours

Implement Redis-based event bus for agent coordination and real-time updates.

**Tasks:**
- Create `server/app/utils/event_bus.py`
- Implement Redis pub/sub wrapper
- Define event types (TaskStarted, TaskProgress, TaskComplete, TaskError)
- Integrate with Agent coordinator
- Add event publishing to API endpoints
- Write tests for event publishing/subscribing

**Dependencies:** Issue #10 (needs agents)
**Blocks:** WebSocket Handler, Agent coordination

---

### Issue: Database Layer for Metadata
**Priority:** HIGH | **Type:** Feature | **Timeline:** 3-4 hours

Add database layer for document metadata and workspace management.

**Tasks:**
- Choose database (SQLite dev / PostgreSQL prod)
- Create SQLAlchemy models
- Add database initialization script
- Implement migrations (Alembic)
- Update API endpoints to use database
- Write database tests

**Files to Create:**
- `server/app/models/database.py`
- `server/app/utils/database.py`
- `server/migrations/`

---

### Issue: WebSocket Handler for Real-time Updates
**Priority:** MEDIUM | **Type:** Feature | **Timeline:** 2-3 hours

Implement WebSocket endpoint for real-time agent task updates.

**Tasks:**
- Create `server/app/api/websocket.py`
- Implement WebSocket endpoint `/ws/agents`
- Subscribe to Event Bus events
- Broadcast events to connected clients
- Add connection management
- Add authentication/authorization
- Write WebSocket tests

**Dependencies:** Event Bus (must exist first)

---

### Issue: Authentication & Authorization Framework
**Priority:** MEDIUM | **Type:** Feature | **Timeline:** 4-6 hours

Implement authentication/authorization for API endpoints.

**Tasks:**
- Choose auth strategy (JWT, API keys, OAuth)
- Implement user model (if needed)
- Add authentication middleware
- Protect sensitive endpoints
- Add rate limiting
- Document auth flow in OpenAPI

**Files to Create:**
- `server/app/auth/` directory
- `server/app/auth/models.py`
- `server/app/auth/middleware.py`

---

### Issue: API Documentation & Usage Guide
**Priority:** MEDIUM | **Type:** Documentation | **Timeline:** 2-3 hours

Create comprehensive API usage guide with examples.

**Tasks:**
- Create `docs/API_USAGE_GUIDE.md`
- Add curl examples for each endpoint
- Add Python client examples
- Document common workflows
- Add error handling examples
- Create Postman/Thunder Client collection

**What Exists:** OpenAPI/Swagger at `/docs`
**What's Needed:** Usage guide with examples

---

## Critical Path & Dependencies

**Recommended Work Order:**

```
Phase 1 Completion (Critical Path):
1. Service Integration (Issue #15) ──┐
                                      ├──> 3. Agent Implementation (Issue #10)
2. Event Bus ─────────────────────────┘

Supporting Work (Parallel):
4. CI/CD Pipeline (Issue #18)
5. Database Layer (not blocking)
```

**Why This Order:**
- **#15 Service Integration:** Makes REST API functional, validates architecture
- **Event Bus:** Required for multi-agent coordination (#10 needs this)
- **#10 Agent Implementation:** Core intelligence, depends on #15 + Event Bus
- **#18 CI/CD:** Can be done anytime, doesn't block other work
- **Database:** Currently using mocks, not critical until production

## Dependencies Graph

**Updated Critical Path (2025-11-06 Review Complete):**

```
Phase 0: Decisions (#1-5) ✅ COMPLETE
    ↓
✅ Issue #15: Service Integration - COMPLETED (close on GitHub)
✅ Issue #9: Vector DB Init - COMPLETED (close on GitHub)
    ↓
🆕 NEW ISSUE: Event Bus Implementation (CRITICAL - Do First)
    ├──> Redis pub/sub
    ├──> Event publishing
    └──> Agent coordination prep
    ↓
Issue #10: Agent Implementation (CRITICAL - Do Second)
    ├──> CREATE missing files (analysis.py, summary.py, recommendation.py)
    ├──> Complete ResearchAgent (needs Event Bus)
    ├──> FIX Coordinator (uncomment agents, pass services)
    └──> FIX main.py (initialize coordinator with services)
    ↓
Phase 1: COMPLETE ──> Phase 2: MCP Integration

Parallel (Supporting Work):
├── Issue #18: CI/CD Pipeline (close #17 duplicate)
├── 🆕 Database Layer (not critical yet)
└── 🆕 WebSocket Handler (depends on Event Bus)

Future Phases (Blocked by Phase 1):
├── Issue #8: Keyword Trends (needs agents from #10)
├── Issue #11: Viz UI (needs backend API working)
└── Phase 2: MCP Integration (needs Phase 1 complete)
```

**Key Insight:** Event Bus is now the #1 blocker. Can't complete agents without it.

## Quick Links

**Repository:** https://github.com/buddha314/babocument

**View all issues:** https://github.com/buddha314/babocument/issues

**Create new issue:** https://github.com/buddha314/babocument/issues/new

**Project board:** (To be created)

## Contributing

When creating new issues:
1. Reference related issues using `#number`
2. Link to relevant documentation files
3. Use descriptive titles
4. Include acceptance criteria for implementation tasks
5. Tag with appropriate phase labels (when available)

## Documentation References

**Planning:**
- [TASKS.md](specs/TASKS.md) - Complete task roadmap
- [PROJECT_STATUS.md](specs/PROJECT_STATUS.md) - Current project state

**Technical Specifications:**
- [VECTOR_DATABASE_SPEC.md](specs/VECTOR_DATABASE_SPEC.md) - Vector DB selection and setup
- [MCP_INTEGRATION_SPEC.md](specs/MCP_INTEGRATION_SPEC.md) - Document repository integration
- [VISUALIZATION_REQUIREMENTS.md](specs/VISUALIZATION_REQUIREMENTS.md) - Data viz requirements

**Implementation Guides:**
- [PLOTLY_BABYLONJS_INTEGRATION.md](docs/PLOTLY_BABYLONJS_INTEGRATION.md) - Plotly + BabylonJS
- [BLENDER_WORKFLOW.md](docs/BLENDER_WORKFLOW.md) - 3D asset pipeline
- [BLENDER_INTEGRATION_PLAN.md](BLENDER_INTEGRATION_PLAN.md) - Asset setup
