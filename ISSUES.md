# GitHub Issues Index

**Repository:** https://github.com/buddha314/babocument/issues

**Last Updated:** 2025-11-06 (Issues #1-5, #9, #12, #15 completed; Issue #18 created for CI/CD; API tests complete)

## Overview

This document provides an organized index of all GitHub issues with direct links and context.

## Phase 0: Foundation & Planning Decisions

Critical architectural decisions that must be made before implementation.

### [Issue #1: Choose client-server communication protocol](https://github.com/buddha314/babocument/issues/1)
**Status:** ✅ DECIDED | **Priority:** High | **Type:** Decision

**Decision Date:** 2025-11-06

Choose between WebSockets (real-time) vs REST API with async (simpler)

**Impact:** Backend architecture, real-time capabilities, agent communication
**Blocking:** Phase 1 server implementation

---

### [Issue #2: Design multi-agent architecture](https://github.com/buddha314/babocument/issues/2)
**Status:** ✅ DECIDED | **Priority:** High | **Type:** Decision

**Decision Date:** 2025-11-06

Design FastAgent multi-agent system for coordinating Research, Analysis, Summary, and Recommendation agents.

**Decisions needed:**
- Agent roles and responsibilities
- Communication patterns
- State management approach

**Impact:** Agent intelligence, system complexity, scalability
**Blocking:** Phase 1 server implementation

---

### [Issue #3: Choose local LLM hosting solution](https://github.com/buddha314/babocument/issues/3)
**Status:** ✅ DECIDED | **Priority:** High | **Type:** Decision

**Decision Date:** 2025-11-06

Select local LLM hosting: Ollama, HuggingFace Transformers, or LangGraph

**Options:**
- **Ollama:** Easy setup, local inference, privacy-focused
- **HuggingFace:** Model hub access, research flexibility
- **LangGraph:** Agentic workflows, state management

**Impact:** Agent capabilities, deployment complexity, hosting costs

---

### [Issue #4: Vector database selection](https://github.com/buddha314/babocument/issues/4)
**Status:** ✅ DECIDED | **Priority:** High | **Type:** Decision

**Decision Date:** 2025-11-06

**Decision:** Use **ChromaDB** with **Sentence Transformers** (all-MiniLM-L6-v2) for vector storage

**Rationale:**
- ✅ Simplest setup (pip install, no separate server)
- ✅ Python-native (perfect for FastAgent backend)
- ✅ Configurable local storage paths
- ✅ Built-in embedding support
- ✅ Free and open source
- ✅ Sufficient performance for 100k+ documents
- ✅ Easy migration path to Weaviate/Qdrant if needed

**Embedding Strategy:**
- **Model:** all-MiniLM-L6-v2 (384 dimensions)
- **Speed:** ~3000 sentences/sec on CPU
- **Quality:** Good for general scientific text
- **Cost:** $0 (local inference)

**Storage Structure:**
```
server/data/chroma/
├── chroma.sqlite3
└── embeddings/
```

**Documentation:** 
- [specs/VECTOR_DATABASE_DECISION.md](specs/VECTOR_DATABASE_DECISION.md) - Decision rationale and implementation
- [specs/VECTOR_DATABASE_SPEC.md](specs/VECTOR_DATABASE_SPEC.md) - Comprehensive analysis

**Next Steps:** 
- Phase 1: Install ChromaDB and implement VectorDatabase wrapper class
- Phase 2: Create initialization script for data/papers corpus
- Phase 3: Integrate with Research Agent for semantic search

**Unblocks:**
- ✅ Issue #9 - Initialize vector database with local papers
- ✅ Phase 1 - Backend setup can proceed
- ✅ Phase 2 - MCP integration can use vector DB for caching
- ✅ Issue #8 - Keyword trend analysis has data source

---

### [Issue #5: MCP integration strategy for document repositories](https://github.com/buddha314/babocument/issues/5)
**Status:** ✅ DECIDED | **Priority:** High | **Type:** Decision

**Decision Date:** 2025-11-06

**Decision:** Hybrid approach using community MCP servers with custom extensions

**Selected Community Servers:**
- **BioMCP** - Primary biomedical source (PubMed + ClinicalTrials.gov + MyVariant.info)
- **arXiv API MCP** - Physics, CS, biology papers with LaTeX support
- **bioRxiv/medRxiv MCP** - Biology and medicine preprints

**Rationale:**
- ✅ Leverage existing, maintained community servers
- ✅ BioMCP purpose-built for biomedical research (perfect match)
- ✅ Faster implementation (weeks vs months)
- ✅ Focus development on Babocument-specific features
- ✅ Build custom servers only when needed

**Documentation:** [specs/MCP_INTEGRATION_DECISION.md](specs/MCP_INTEGRATION_DECISION.md) (6 KB)

**Implementation Plan:**
- **Week 1-2:** Install and test 3 community MCP servers
- **Week 3-4:** Build Research Agent with unified interface
- **Week 5-6:** Integrate vector database and caching
- **Week 7-8:** Create API endpoints

**Impact:** Accelerates Phase 2 (data integration), enables Phase 5 (intelligence features)

**Next Steps:** Begin Phase 1 MCP server installation and testing

---

### [Issue #6: Plotly.js integration strategy for 3D visualization](https://github.com/buddha314/babocument/issues/6)
**Status:** 🟡 Open | **Priority:** Medium | **Type:** Decision

Determine how to integrate Plotly.js scientific visualizations into BabylonJS 3D scenes

**Strategies:**
- **A:** Canvas texture mapping (best for VR)
- **B:** HTML overlay (best for desktop)
- **C:** Native BabylonJS conversion (maximum performance)
- **Recommended:** Hybrid (auto-detect mode)

**Documentation:** [docs/PLOTLY_BABYLONJS_INTEGRATION.md](docs/PLOTLY_BABYLONJS_INTEGRATION.md) (16 KB)

**Impact:** Visualization capabilities, performance, UX

---

### [Issue #7: Setup Blender asset pipeline](https://github.com/buddha314/babocument/issues/7)
**Status:** 🟡 Open | **Priority:** Medium | **Type:** Setup

Establish Blender → GLTF 2.0 → GLB export workflow for 3D assets

**Tasks:**
- Create directory structure for .blend sources and .glb exports
- Document export settings
- Update .gitignore
- Create contributor guidelines

**Assets needed:**
- Phase 3: File Room environment
- Phase 4: Librarian character (rigged, animated)
- Phase 7: Lab equipment models

**Documentation:**
- [BLENDER_INTEGRATION_PLAN.md](BLENDER_INTEGRATION_PLAN.md)
- [docs/BLENDER_WORKFLOW.md](docs/BLENDER_WORKFLOW.md) (7 KB)

---

## Feature Implementation Issues

### [Issue #8: Implement keyword trend line graphs](https://github.com/buddha314/babocument/issues/8)
**Status:** 🟡 Open | **Priority:** High | **Type:** Feature

Enable Beabadoo to visualize keyword frequency trends over time across research corpus

**User Story:**
> As Beabadoo, I want to see how frequently specific keywords appear in research papers over time, so I can understand the evolution and popularity of research topics in biomanufacturing.

**Features:**
- Compare up to 10 keywords simultaneously
- Interactive hover, zoom, pan
- Export as PNG/SVG and CSV/JSON
- Desktop (HTML overlay) and VR (3D texture) modes

**Phases:** 5 (Backend), 3 & 6 (Frontend)

**Dependencies:** [#6](#issue-6-plotlyjs-integration-strategy-for-3d-visualization), [#4](#issue-4-vector-database-selection)

**Documentation:** [specs/VISUALIZATION_REQUIREMENTS.md](specs/VISUALIZATION_REQUIREMENTS.md)

---

### [Issue #9: Initialize vector database with local papers](https://github.com/buddha314/babocument/issues/9)
**Status:** ✅ COMPLETED | **Priority:** High | **Type:** Implementation
**Completed:** 2025-11-06

Create initialization script to populate vector database from data/papers directory

**Completed:**
- ✅ Parse PDFs from `data/papers/` (4 papers indexed)
- ✅ Extract full text and metadata
- ✅ Generate embeddings using Sentence Transformers (all-MiniLM-L6-v2)
- ✅ Configurable storage paths (server/data/chroma/)
- ✅ Semantic search functionality implemented and tested

**Deliverables:**
- `server/scripts/init_vector_db.py` - Initialization script
- `server/scripts/test_vector_search.py` - Search testing script
- `server/app/services/vector_db.py` - ChromaDB service wrapper
- 4 papers from data/papers/ successfully indexed

**Phases:** 1 (Backend - Complete)

**Dependencies:** [#4](#issue-4-vector-database-selection) ✅

**Documentation:** [specs/VECTOR_DATABASE_SPEC.md](specs/VECTOR_DATABASE_SPEC.md)

---

### [Issue #12: Develop devcontainer for server application](https://github.com/buddha314/babocument/issues/12)
**Status:** ✅ Completed | **Priority:** High | **Type:** DevOps
**Completed:** 2025-11-06

Create development container configuration for FastAgent server with all Python dependencies and MCP server integrations.

**Requirements:**
- Python 3.11+ environment
- FastAgent dependencies
- ChromaDB and vector database tools
- MCP server integration support
- Development tools and extensions

**Deliverables:**
- `.devcontainer/devcontainer.json` - Container configuration
- `server/requirements.txt` - Python dependencies
- Documentation in README.md

**Benefits:**
- Consistent development environment
- Simplified onboarding for contributors
- Isolated dependency management
- Works with VS Code Remote Containers

**Phases:** 0 (DevOps), applies to Phase 1+

**Dependencies:** None (can implement immediately)

---

### [Issue #14: Select optimal local LLMs for research paper analysis](https://github.com/buddha314/babocument/issues/14)
**Status:** 🟡 Open | **Priority:** High | **Type:** Decision

Evaluate and select specific local LLM models for different agent tasks in the multi-agent system.

**Agent-Specific Requirements:**
- **Research Agent:** Query understanding, semantic search
- **Analysis Agent:** Trend analysis, pattern detection
- **Summary Agent:** Document summarization, key insight extraction
- **Recommendation Agent:** Related paper suggestions, gap identification

**Evaluation Criteria:**
- Model size vs performance trade-offs
- Inference speed for real-time responses
- Context window size for long documents
- Fine-tuning potential for scientific domain
- Local hosting feasibility

**Candidate Models:**
- Llama 3.1 (8B, 70B variants)
- Mistral 7B / Mixtral 8x7B
- Qwen 2.5 (specialized models)
- Domain-specific models (BioGPT, SciBERT embeddings)

**Impact:** Agent intelligence quality, response speed, resource requirements

**Dependencies:** [#3](#issue-3-choose-local-llm-hosting-solution) (hosting solution)

---

### [Issue #15: Implement REST API endpoints for document and repository management](https://github.com/buddha314/babocument/issues/15)
**Status:** ✅ COMPLETED | **Priority:** High | **Type:** Feature | **Completion Date:** 2025-11-06

**User Story:**
> As a developer/user, I need REST API endpoints to view, save, and manage documents and repositories, so that the multi-agent system can perform document operations programmatically.

**Completed Implementation:**

**API Modules Created:**
- ✅ `server/app/api/documents.py` - 7 endpoints for document CRUD and search
- ✅ `server/app/api/repositories.py` - 5 endpoints for repository management
- ✅ `server/app/api/stats.py` - 5 endpoints for statistics and status

**Test Coverage:**
- ✅ 60 passing tests across all endpoints
- ✅ 84% code coverage (301 statements, 48 missed)
- ✅ All response models validated with Pydantic
- ✅ Error handling tested (404, 400, 422, 500)

**Documentation:**
- ✅ OpenAPI/Swagger docs at `/docs`
- ✅ SESSION_2025-11-06_REST_API_IMPLEMENTATION.md
- ✅ SESSION_2025-11-06_REST_API_TESTS.md

**Next Steps:**
- Implement Event Bus for agent coordination
- Connect endpoints to Vector DB and LLM services
- Add database layer for metadata storage

---

## Phase 1: DevOps & Infrastructure

### [Issue #18: Implement CI/CD pipeline with GitHub Actions](https://github.com/buddha314/babocument/issues/18)
**Status:** 🟡 Open | **Priority:** High | **Type:** Enhancement

**Summary:**
Implement automated CI/CD pipeline using GitHub Actions to build, test, and validate both the server (Python/FastAPI) and client (Next.js/BabylonJS) components on every push and pull request.

**Requirements:**

**Server Pipeline:**
- Run pytest with 84% coverage requirement
- Python 3.13 environment
- Linting (flake8/black/mypy)

**Client Pipeline:**
- Next.js build validation
- Node.js 18+ environment
- ESLint and TypeScript checking

**Deliverables:**
- `.github/workflows/server-ci.yml`
- `.github/workflows/client-ci.yml`
- Coverage reports as artifacts
- PR status checks
- CI/CD badges in README

**Dependencies:**
- ✅ Issue #15 (REST API) - COMPLETED
- ✅ API test suite - COMPLETED (60 tests, 84% coverage)

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
**Status:** 🟡 Open | **Priority:** High | **Type:** Epic
**Timeline:** 1-2 weeks

Initialize Python backend with FastAgent framework and multi-agent coordination

**Prerequisites:** Issues #1, #2, #3, #4 (all Phase 0 decisions)

**Major tasks:**
- Initialize Python project structure
- Set up FastAgent framework
- Implement agent coordinator/orchestrator
- Create base agent classes
- Define API endpoints
- Configure vector database integration
- Set up logging and monitoring

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

**Total Issues:** 15

**Completed:** 7 (Issues #1, #2, #3, #4, #5, #9, #12)

**By Type:**
- 🔷 Decisions: 7 (Issues #1-#6, #14) - 5 decided, 2 open
- 🔶 Setup: 1 (Issue #7)
- ⚙️ Features: 4 (Issues #8, #9, #15) - 1 completed, 3 open
- 📦 Epics: 2 (Issues #10-#11)
- 🛠️ DevOps: 1 (Issue #12) - completed

**By Priority:**
- 🔴 High: 13 (7 completed, 6 open)
- 🟡 Medium: 2

**By Phase:**
- Phase 0 (Planning): 7 decision issues (5 decided, 2 open)
- Phase 1 (Backend): 2 features (Issue #10 epic in progress, Issue #15 new), 1 implementation (completed)
- Phase 2 (Data): 0 open
- Phase 3 (Frontend): 1 epic, 1 feature
- Phase 4 (Librarian): 0 (future)
- Phase 5 (Intelligence): 0 (future)
- Phase 6 (Management): 0 (future)

## Dependencies Graph

```
Phase 0 Decisions (#1, #2, #3, #4, #5 - DECIDED)
    ↓
Issue #15 (REST API Implementation) - ✅ COMPLETED
    ↓
Issue #18 (CI/CD Pipeline) - 🟡 NEW
    ↓
Issue #14 (Select specific LLM models)
    ↓
Issue #10 (Phase 1: Backend Setup) - 🟡 In Progress
    ↓
Issue #9 (Initialize Vector DB) - ✅ COMPLETED
    ↓
Phase 2: MCP Integration (uses #5 decision)
    ↓
Issue #8 (Keyword Trends - Phase 5)
    ↓
Issue #11 (Visualization UI - Phase 3, needs #6 decision)
```

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
