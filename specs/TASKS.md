# Task Tracking - Babocument

**Last Updated:** 2025-11-06
**Current Phase:** Phase 1 (Server Foundation) - 45% Complete
**Status:** Active Development - Vector DB Complete

## Project Status Summary

**Phase 0 (Planning):** 86% Complete (6/7 decisions made)
- ✅ Communication Protocol (REST + WebSocket)
- ✅ Multi-Agent Architecture (Event-driven coordinator)
- ✅ LLM Hosting (Ollama + LiteLLM)
- ✅ Vector Database (ChromaDB)
- ✅ MCP Integration (Community servers)
- ✅ Launch Script (PowerShell)
- 🟡 Plotly Integration (analysis complete, decision pending)
- 🟡 Blender Pipeline (planning stage)
- 🆕 Issue #14: LLM Model Selection (new, depends on Issue #3)

**Phase 1 (Backend):** 45% Complete (foundation + Vector DB complete)
- ✅ Python environment configured
- ✅ FastAPI application structure
- ✅ Agent base classes and coordinator
- ✅ Vector DB service (ChromaDB with 4 papers indexed)
- 🟡 LLM Client, Event Bus services (next priorities)

**Next Milestones:**
1. Complete Phase 1 backend services (✅ Vector DB, LLM Client, Event Bus)
2. Implement Phase 2 MCP server integrations
3. ✅ Initialize vector database with local papers (Issue #9 - COMPLETE)
4. Begin Phase 3 client visualization work

**Documentation:**
- ISSUES.md - Synced with GitHub (Issues #1-14)
- SESSION_HANDOFF.md - Latest session details
- Decision docs in specs/ - Complete for Phase 0

## Critical Path Tasks

### Phase 0: Foundation & Planning (86% Complete)
**Goal:** Establish technical foundation and make key architectural decisions

- [x] Initialize git repository
- [x] Create .gitignore for project stack
- [x] Document current project state
- [x] **DECISION COMPLETE:** Choose client-server communication protocol
  - ✅ **Decision:** Hybrid REST + WebSocket approach
  - REST for CRUD operations, WebSocket for real-time agent updates
  - Documentation: specs/COMMUNICATION_PROTOCOL_DECISION.md
  - Issue #1: https://github.com/buddha314/babocument/issues/1
- [x] **DECISION COMPLETE:** Design multi-agent architecture
  - ✅ **Decision:** Event-driven coordinator pattern with FastAgent
  - Agent roles: Research, Analysis, Summary, Recommendation
  - Redis pub/sub for event bus
  - Documentation: specs/MULTI_AGENT_ARCHITECTURE.md
  - Issue #2: https://github.com/buddha314/babocument/issues/2
- [x] **DECISION COMPLETE:** Choose local LLM hosting solution
  - ✅ **Decision:** Ollama with LiteLLM gateway
  - Models: llama3.2:3b (summaries), qwen2.5:7b (chat), mistral:7b (instructions)
  - Zero cloud costs, privacy-first, easy model switching
  - Documentation: specs/LLM_HOSTING_DECISION.md
  - Issue #3: https://github.com/buddha314/babocument/issues/3
- [x] **DECISION COMPLETE:** Vector database selection and configuration
  - ✅ **Decision:** ChromaDB with Sentence Transformers (all-MiniLM-L6-v2)
  - Embedded database, no separate server required
  - 384-dimensional embeddings, ~3000 sentences/sec on CPU
  - Storage: server/data/chroma/
  - Documentation: specs/VECTOR_DATABASE_DECISION.md
  - Issue #4: https://github.com/buddha314/babocument/issues/4
- [x] **DECISION COMPLETE:** MCP integration for document repositories
  - ✅ **Decision:** Hybrid approach using community MCP servers
  - BioMCP (PubMed + ClinicalTrials.gov), arXiv API MCP, bioRxiv/medRxiv MCP
  - Custom extensions only for Babocument-specific features
  - Documentation: specs/MCP_INTEGRATION_DECISION.md
  - Issue #5: https://github.com/buddha314/babocument/issues/5
- [x] **COMPLETED:** Launch script for unified development workflow
  - ✅ PowerShell script: launch.ps1
  - Starts client and server with dependency checks
  - Supports --client-only flag for current phase
  - Documentation: ISSUE_12_LAUNCH_SCRIPT.md
  - Issue #12: https://github.com/buddha314/babocument/issues/12
- [ ] **DECISION REQUIRED:** Select optimal local LLMs for research paper analysis
  - Evaluate specific models for each agent task
  - Consider: Llama 3.1, Mistral, Qwen, domain-specific models
  - Balance model size vs performance trade-offs
  - Issue #14: https://github.com/buddha314/babocument/issues/14
  - Depends on Issue #3 (hosting solution) - COMPLETED
- [ ] **DECISION REQUIRED:** Plotly integration strategy for 3D visualization
  - Determine Plotly.js integration with BabylonJS
  - Options: Canvas texture mapping, HTML overlay, or native BabylonJS
  - Impact: Visualization capabilities, performance, VR/desktop UX
  - Documentation: docs/PLOTLY_BABYLONJS_INTEGRATION.md (analysis complete)
  - Issue #6: https://github.com/buddha314/babocument/issues/6
- [ ] **Set up Blender asset pipeline**
  - Establish directory structure for `.blend` source files and `.glb` exports
  - Document GLTF 2.0 export workflow for BabylonJS
  - Update .gitignore for Blender files
  - Documentation: BLENDER_INTEGRATION_PLAN.md, docs/BLENDER_WORKFLOW.md
  - Issue #7: https://github.com/buddha314/babocument/issues/7
- [ ] Define API contract/specifications (can start now)
- [ ] Create technical architecture document (partially complete)

### Phase 1: Server Foundation (30% Complete - In Progress)
**Goal:** Set up FastAgent backend with basic agent coordination

**Prerequisites:** ✅ Phase 0 decisions complete (6/7 decided)

**Environment Setup:**
- [x] Initialize Python project structure in /server
- [x] Set up Python virtual environment (server/venv/)
- [x] Install all dependencies (FastAPI, ChromaDB, LiteLLM, PyTorch, etc.)
- [x] Configure environment variables (.env, .env.example)
- [x] Create comprehensive setup documentation (server/README.md, server/SETUP.md)

**Core Backend:**
- [x] Set up FastAPI application (server/app/main.py)
  - Structured logging with structlog
  - CORS configuration
  - Health check endpoints
- [x] Implement Pydantic configuration management (server/app/config.py)
- [x] Create base agent class with event publishing (server/app/agents/base.py)
- [x] Implement agent coordinator skeleton (server/app/agents/coordinator.py)
- [x] Create Research Agent skeleton (server/app/agents/research.py)
- [x] Set up package structure (api, models, services, utils)

**Remaining Tasks:**
- [x] Implement Vector Database Client (server/app/services/vector_db.py)
  - ✅ ChromaDB wrapper with initialization
  - ✅ Document ingestion from data/papers/
  - ✅ Semantic search implementation
  - ✅ Issue #9: https://github.com/buddha314/babocument/issues/9
  - ✅ Initialization script (server/scripts/init_vector_db.py)
  - ✅ Search testing (4 papers indexed, semantic search working)
- [x] Implement LLM Client (server/app/services/llm_client.py)
  - ✅ LiteLLM wrapper with Ollama integration
  - ✅ Model selection per agent type
  - ✅ Summarization and chat functions
  - ✅ Query parsing and keyword extraction
  - ✅ Error handling and retries
- [ ] Implement REST API endpoints (server/app/api/)
  - Document CRUD operations (list, get, upload, delete)
  - Repository management (list, status, sync)
  - Search endpoints (keyword and semantic)
  - Statistics and status endpoints
  - Issue #15: https://github.com/buddha314/babocument/issues/15
- [ ] Implement Event Bus (server/app/utils/event_bus.py)
  - Redis pub/sub for agent coordination
  - Event publishing/subscribing
  - Task progress updates
- [ ] Implement Event Bus (server/app/utils/event_bus.py)
  - Redis pub/sub for agent coordination
  - Event publishing/subscribing
  - Task progress updates
- [ ] Implement REST API endpoints (server/app/api/rest.py)
  - POST /api/v1/search (initiate search)
  - GET /api/v1/search/{task_id} (get status)
  - POST /api/v1/summarize (summarize document)
  - GET /api/v1/agents/status (agent health)
  - Issue #15: Document and repository management
- [ ] Implement WebSocket handler (server/app/api/websocket.py)
  - /ws/agents (real-time task updates)
  - Subscribe to task progress events
  - Broadcast to connected clients
- [ ] Complete agent implementations
  - Research Agent - Vector DB + MCP search
  - Analysis Agent - Trend analysis (Issue #8)
  - Summary Agent - LLM summarization
  - Recommendation Agent - Related papers
- [ ] Set up required services
  - Redis server for event bus
  - Ollama with downloaded models
- [x] Implement basic logging and monitoring (structlog integrated)
- [x] Create initialization script for data/papers ingestion

**Current Status:** Vector DB and LLM Client complete! Ready for Event Bus and REST API implementation.

**Next Steps:**
1. ✅ Vector DB Client implemented and tested (4 papers indexed)
2. ✅ LLM Client implemented (summarization, chat, keyword extraction, query parsing)
3. Implement REST API endpoints (priority #1 - Issue #15)
4. Start Redis server: `docker run -d -p 6379:6379 --name babocument-redis redis:7-alpine`
5. Download Ollama models: `ollama pull llama3.2:3b`, `ollama pull qwen2.5:7b`
6. Implement Event Bus (priority #2)
7. Test end-to-end workflows

**Documentation:**
- Session details: SESSION_2025-11-06_PHASE1_INIT.md
- Setup guide: server/README.md, server/SETUP.md
- Architecture: specs/MULTI_AGENT_ARCHITECTURE.md

**Estimated Timeline:** 1-2 weeks remaining (started 2025-11-06)

### Phase 2: Data Source Integration
**Goal:** Connect to external research data sources

**Prerequisites:** Phase 1 complete

**MCP Server Integration** (Based on Issue #5 Decision):
- [ ] Set up BioMCP server (Primary biomedical source)
  - Install and configure BioMCP
  - Configure NCBI API key
  - PubMed access
  - ClinicalTrials.gov integration
  - MyVariant.info support
- [ ] Set up arXiv API MCP server
  - Install arXiv MCP server
  - Configure rate limiting (1 req per 3 sec)
  - LaTeX/math support for complex equations
- [ ] Set up bioRxiv/medRxiv MCP servers
  - Install bioRxiv MCP server
  - Install medRxiv MCP server
  - Configure preprint access
- [ ] Implement unified Research Agent interface
  - Multi-source search coordination
  - Result deduplication by DOI
  - Standardized metadata format
  - Rate limiting and retry logic
- [ ] Build data normalization/transformation layer
  - Convert MCP responses to standard format
  - Extract and normalize metadata
  - Handle missing fields gracefully

**Vector Database Integration:**
- [ ] Initialize vector database with local papers (Issue #9)
  - Parse PDFs from data/papers directory
  - Extract text and metadata
  - Generate embeddings using all-MiniLM-L6-v2
  - Store in ChromaDB for semantic search
  - Create initialization script: server/scripts/init_vector_db.py
- [ ] Implement caching strategy
  - Cache paper metadata in vector DB
  - Cache full-text content
  - Semantic search across cached papers
  - Cache hit rate monitoring

**API Development:**
- [ ] Create REST API endpoints
  - POST /api/papers/search (multi-source search)
  - GET /api/papers/{paper_id} (get full paper)
  - GET /api/papers/sources (list available sources)
- [ ] Add error handling and logging
- [ ] Implement rate limiting middleware

**Documentation:** specs/MCP_INTEGRATION_DECISION.md, specs/VECTOR_DATABASE_DECISION.md

**Estimated Timeline:** 1-2 weeks

### Phase 3: Client - Virtual Environment
**Goal:** Build the immersive File Room experience

**Prerequisites:** Basic server API available

- [ ] Design File Room spatial layout
  - Corridor dimensions and structure
  - Year partition placement algorithm
  - Camera movement system
- [ ] Implement timeline corridor in BabylonJS
  - Procedural corridor generation
  - Glass partition rendering
  - Year labels and markers
- [ ] Create navigation system
  - Walking mechanics
  - Teleportation (if VR)
  - Camera controls
- [ ] Implement document visualization
  - Document cards/panels in 3D space
  - Hover effects and interactions
  - Selection and preview
- [ ] Implement data visualization UI
  - Word cloud display
  - Keyword trend line graphs (2D and 3D)
  - Interactive chart controls
  - Plotly.js integration for scientific plotting
  - 3D scatter plots, surface plots, and heatmaps
  - Render plots as textures on 3D panels or native BabylonJS meshes
- [ ] Add lighting and atmosphere
  - Ambient lighting design
  - Glass material shaders
  - Fog/depth effects

**Estimated Timeline:** 2-3 weeks

### Phase 4: Librarian Character
**Goal:** Animated guide character for user interaction

**Prerequisites:** Phase 3 foundation

- [ ] Design Librarian character concept
- [ ] Create 3D character model (Blender/external)
- [ ] Rig character for animation
- [ ] Create animation set
  - Idle animations
  - Gesture animations
  - Walking/floating animations
  - Interaction animations
- [ ] Integrate character into BabylonJS scene
- [ ] Implement character AI/behavior system
- [ ] Add speech/dialogue system
- [ ] Create character-user interaction patterns

**Estimated Timeline:** 2-3 weeks

### Phase 5: Agent Intelligence
**Goal:** Implement specialized research agents

**Prerequisites:** Phase 2 complete

- [ ] Research Agent
  - Query understanding and parsing
  - Multi-source search coordination (MCP + Vector DB)
  - Result ranking and relevance scoring
  - Deduplication across sources
- [ ] Analysis Agent
  - Trend analysis over time
  - Word cloud generation from corpus
  - **Keyword trend line graphs (Issue #8)**
    - Track keyword frequency over time
    - Compare up to 10 keywords simultaneously
    - Interactive visualization (hover, zoom, pan)
    - Export as PNG/SVG and CSV/JSON
    - Desktop (HTML overlay) and VR (3D texture) modes
  - Correlation detection across papers
  - Temporal pattern recognition
- [ ] Summary Agent
  - Article summarization using LLM
  - Key insight extraction
  - Workspace summary generation
  - Abstract generation
- [ ] Recommendation Agent
  - Related paper suggestions based on similarity
  - Research direction recommendations
  - Gap identification in literature
  - Citation network analysis

**Documentation:** 
- specs/VISUALIZATION_REQUIREMENTS.md (keyword trends)
- specs/MULTI_AGENT_ARCHITECTURE.md (agent design)

**Estimated Timeline:** 3-4 weeks

### Phase 6: Document Management
**Goal:** Workspace and document interaction features

**Prerequisites:** Phase 3, Phase 5 partially complete

- [ ] Workspace system
  - Create workspace API
  - Workspace persistence (database)
  - Workspace sharing/collaboration
  - Workspace metadata and settings
- [ ] **Journal repository management** (NEW - added 2025-11-06)
  - List all configured repositories
  - Add/edit/remove journal repositories dynamically
  - Test repository connectivity and health
  - Repository configuration UI/API
  - Enable/disable repositories per workspace
  - API: GET/POST/PUT/DELETE /api/repositories
  - Documentation: specs/VISUALIZATION_REQUIREMENTS.md Section 4
- [ ] **Workspace-scoped repository collections** (NEW - added 2025-11-06)
  - Assign repositories to workspaces
  - Configure workspace-specific source sets
  - Track repository usage per workspace
  - Repository contribution analytics
  - API: GET/PUT /api/workspaces/{id}/repositories
- [ ] Document operations
  - Open and view documents in VR environment
  - Annotation system for papers
  - Save document summaries
  - Tag and categorize documents
  - Document versioning
- [ ] Association tracking
  - Link documents to workspaces
  - Track document relationships (citations, references)
  - Visualize connection graphs
  - Document clustering by topic
- [ ] Search and filter
  - Full-text search across cached papers
  - Metadata filtering (year, author, journal)
  - Timeline-based queries (papers by year)
  - **Repository-scoped searches per workspace**
  - Advanced query syntax
- [ ] Analytics and visualization
  - Generate word clouds from corpus
  - Display keyword trend line graphs over time (Issue #8)
  - Export trend data and visualizations
  - Citation network visualization
  - Research landscape heatmaps

**Documentation:**
- specs/VISUALIZATION_REQUIREMENTS.md (Section 4: Repository Management)
- Updated: README.md, PROJECT_STATUS.md (repository features)

**Estimated Timeline:** 2-3 weeks

### Phase 7: Virtual Labs
**Goal:** Collaborative spaces and 3D equipment models

**Prerequisites:** Phase 3 complete

- [ ] Design virtual lab spaces
- [ ] Create lab room templates
- [ ] Model laboratory equipment (Blender)
  - Bioreactors
  - Microscopes
  - Lab benches
  - Equipment specific to biomanufacturing
- [ ] Implement multi-user presence (if collaborative)
- [ ] Add equipment interaction systems
- [ ] Create equipment information panels

**Estimated Timeline:** 2-3 weeks

### Phase 8: Advanced Features
**Goal:** Polish and advanced capabilities

**Prerequisites:** Phases 1-6 complete

- [ ] Video upload and processing
  - Upload interface
  - Text extraction (OCR)
  - Image extraction
  - Video metadata analysis
- [ ] Timeline visualization enhancements
  - Interactive timeline controls
  - Zoom and filter capabilities
  - Animation and transitions
  - Keyword trend line graphs overlay
  - Temporal data scrubbing
- [ ] MCP integrations
  - Blender MCP plugin
  - BabylonJS Editor integration
  - Asset pipeline automation
- [ ] Performance optimization
  - Asset loading optimization
  - LOD system
  - Memory management
- [ ] User authentication
- [ ] Analytics and telemetry

**Estimated Timeline:** 3-4 weeks

## Backlog / Future Considerations

- [ ] Mobile/tablet support
- [ ] Offline mode capabilities
- [ ] Export capabilities (PDF reports, data exports)
- [ ] Advanced collaboration features (live co-browsing)
- [ ] Voice interaction with Librarian
- [ ] AR mode for mobile devices
- [ ] Integration with more data sources
- [ ] Custom agent creation by users
- [ ] Workspace templates
- [ ] Tutorial/onboarding experience

## Blocked Tasks

**Phase 0 Blockers - RESOLVED ✅**
- ✅ Issue #1 (Communication Protocol) - DECIDED
- ✅ Issue #2 (Multi-Agent Architecture) - DECIDED
- ✅ Issue #3 (LLM Hosting) - DECIDED
- ✅ Issue #4 (Vector Database) - DECIDED
- ✅ Issue #5 (MCP Integration) - DECIDED

**Phase 1 - UNBLOCKED - Ready to Implement ✅**
- All critical decisions complete
- Python environment configured
- Backend structure initialized
- Next: Implement services (Vector DB, LLM, Event Bus)

**Currently Blocked (Lower Priority):**
- **Phase 3 (Client Visualization)** - Needs Issue #6 (Plotly integration strategy)
- **Phase 4 & 7 (3D Assets)** - Needs Issue #7 (Blender asset pipeline)

**Not Blocking Critical Path:**
- Issue #14 (Select specific LLM models) - Can proceed with default models from Issue #3

## Questions to Resolve

### High Priority (Affects Current Work)

1. ✅ **Communication Protocol:** WebSockets vs REST+async? **RESOLVED**
   - Decision: Hybrid approach (REST + WebSocket)
   - Documentation: specs/COMMUNICATION_PROTOCOL_DECISION.md

2. ✅ **Agent Framework:** Custom vs existing FastAgent patterns? **RESOLVED**
   - Decision: Event-driven coordinator with Redis pub/sub
   - Documentation: specs/MULTI_AGENT_ARCHITECTURE.md

3. ✅ **Vector Database:** Which vector DB and embedding model? **RESOLVED**
   - Decision: ChromaDB with all-MiniLM-L6-v2
   - Documentation: specs/VECTOR_DATABASE_DECISION.md

4. ✅ **LLM Hosting:** Local vs cloud? **RESOLVED**
   - Decision: Ollama with LiteLLM gateway
   - Documentation: specs/LLM_HOSTING_DECISION.md

5. ✅ **MCP Integration:** Build custom vs use community servers? **RESOLVED**
   - Decision: Hybrid - use community servers (BioMCP, arXiv, bioRxiv)
   - Documentation: specs/MCP_INTEGRATION_DECISION.md

### Medium Priority (Can Decide Later)

6. **Plotly Integration:** How to integrate with BabylonJS?
   - Options analyzed: Canvas texture, HTML overlay, native conversion
   - Documentation: docs/PLOTLY_BABYLONJS_INTEGRATION.md (analysis complete)
   - Decision pending: Issue #6

7. **3D Asset Pipeline:** Blender workflow and optimization?
   - Affects: Phase 4 (Librarian) and Phase 7 (Lab equipment)
   - Documentation: BLENDER_INTEGRATION_PLAN.md, docs/BLENDER_WORKFLOW.md
   - Decision pending: Issue #7

8. **LLM Model Selection:** Which specific models for each agent?
   - Base recommendation from Issue #3, can refine
   - Affects: Agent performance and quality
   - Can test and iterate: Issue #14

## Definition of Done

A task is considered "done" when:
- [ ] Code is written and tested
- [ ] Documentation is updated
- [ ] Code review completed (if applicable)
- [ ] Integration tests pass
- [ ] User-facing features are tested with persona in mind
- [ ] Performance benchmarks met
- [ ] Committed to git with clear message

## Notes

- All estimates are preliminary and subject to change
- Dependencies may shift as architecture solidifies
- Regular reviews recommended at end of each phase
- Beabadoo persona should inform all UX decisions

## Maintenance

**⚠️ CRITICAL: START EVERY SESSION WITH SYNC CHECK ⚠️**

Before starting any work, ALWAYS sync these three sources:
1. **GitHub Issues** (run `gh issue list --state all`)
2. **ISSUES.md** (update status, counts, timestamps)
3. **TASKS.md** (mark checkboxes, update percentages)

See SESSION_HANDOFF.md for complete sync checklist.

**This document should be kept in sync with:**
- ISSUES.md - GitHub issues index (check for new/closed issues)
- SESSION_HANDOFF.md - Latest session work and status
- PROJECT_STATUS.md - Overall project state
- Decision documents in specs/ - Architectural decisions

**Update triggers:**
- **START OF EVERY SESSION** (mandatory sync check)
- When GitHub issues are created/updated/closed
- After completing major milestones or phases
- When architectural decisions are made
- At the end of each development session

**Last sync:** 2025-11-06 - Vector DB complete, LLM Client complete, Issue #15 created for REST API
