# Project Task List - Babocument

**Last Updated:** 2025-11-06 (Event Bus Complete)
**Current Phase:** Phase 1 Backend - 85% Complete
**GitHub Issues:** 18 open | 10 closed

**🎯 CRITICAL PATH:**
1. ~~Issue #19: Event Bus~~ ✅ **COMPLETE** (3 hrs)
2. Issue #10: Agents (6-8 hrs) ← **DO NEXT**
3. **Phase 1 Complete!** (100%)

**📊 See PRIORITY_ANALYSIS_2025-11-06.md for complete details**

---

## P0 - CRITICAL (Blocking Phase 1 & 2)

### ~~Issue #19: Event Bus Implementation~~ ✅ **COMPLETED**
- **Time:** 3 hours (completed)
- **Status:** ✅ Complete
- **Completed:** 2025-11-06
- **Link:** https://github.com/buddha314/babocument/issues/19

Redis pub/sub for agent coordination implemented with tests. See HANDOFF_2025-11-06_EVENT_BUS.md

### Issue #10: Complete Agents ⭐ **DO NEXT (Backend)**
- **Time:** 6-8 hours  
- **Status:** 25% (base classes only)
- **Depends on:** ~~#19~~ ✅
- **Link:** https://github.com/buddha314/babocument/issues/10

**CRITICAL:** Create missing files (analysis.py, summary.py, recommendation.py), complete research.py, fix coordinator initialization.

---

## P0 - CRITICAL (Client-Server Integration - NEW)

### Issue #30: Client API Infrastructure Setup ⭐ **NEW**
- **Time:** 4-6 hours
- **Status:** Not started
- **Phase:** Phase 2 - Client Development
- **Link:** TBD

Set up API client infrastructure for BabylonJS client to communicate with FastAPI server.

**Tasks:**
- Install dependencies (axios, @tanstack/react-query, zod)
- Create base API client with interceptors
- Define TypeScript types from OpenAPI schema
- Set up React Query provider
- Configure environment variables
- Test server connectivity

**Files to Create:**
- `client/src/lib/api/client.ts`
- `client/src/lib/api/types.ts`
- `client/src/app/providers.tsx`
- `client/.env.local`

**Deliverables:** Working API client that can communicate with server

### Issue #32: Document API Integration ⭐ **NEW**
- **Time:** 8-12 hours
- **Status:** Not started
- **Depends on:** #30
- **Link:** TBD

Implement document management features in client using server REST API.

**Tasks:**
- Create `documents.ts` API methods
- Create React Query hooks (useDocuments, useDocument, useSearch)
- Build DocumentList component
- Build DocumentViewer component
- Build DocumentUploader component
- Test CRUD operations

**Files to Create:**
- `client/src/lib/api/documents.ts`
- `client/src/lib/hooks/useDocuments.ts`
- `client/src/components/documents/DocumentList.tsx`
- `client/src/components/documents/DocumentViewer.tsx`
- `client/src/components/documents/DocumentUploader.tsx`

**Deliverables:** Functional document management UI

---

## P1 - HIGH (Required for Production & Client Integration)

### Issue #33: Search Integration (Client) ⭐ **NEW**
- **Time:** 6-8 hours
- **Status:** Not started
- **Depends on:** #32
- **Link:** TBD

Implement semantic and keyword search in client with UI components.

**Tasks:**
- Create search API methods
- Create useSearch hook
- Build SearchBar component
- Build SearchResults component
- Add filters (year, source, type)
- Test semantic & keyword search
- Integrate with 3D scene

**Deliverables:** Functional search UI with result highlighting

### Issue #38: Agent-Assisted Paper Discovery ⭐ **NEW**
- **Time:** 14-20 hours (Backend: 8-12, Frontend: 6-8)
- **Status:** Not started
- **Depends on:** #10 (Agents), #32 (Document API)
- **Link:** TBD

Enable natural language queries for finding scientific papers using AI agents.

**User Story:** "As Beabadoo, I want to ask the agent to find scientific papers for me using natural language."

**Tasks:**
- Enhance Research Agent with NLP query processing
- Add intent extraction (keywords, authors, time ranges)
- Create agent search API endpoints
- Build AgentSearchBar UI component
- Build AgentSearchResults with AI explanations
- Add "why this matches" explanations
- Support voice input in VR
- Integrate with existing search

**Example Queries:**
- "Find papers about bioink formulation for 3D printing"
- "Show me recent advances in CRISPR gene editing"
- "Compare different methods for tissue scaffolding"

**Deliverables:** Natural language search with AI-powered results

### Issue #34: WebSocket Real-time Updates (Client) ⭐ **NEW**
- **Time:** 4-6 hours
- **Status:** Not started
- **Depends on:** #30, Server #21 (WebSocket Handler)
- **Link:** TBD

Implement WebSocket connection for real-time agent updates and task progress.

**Tasks:**
- Create WebSocket manager with auto-reconnect
- Create useWebSocket hook
- Subscribe to event types (task progress, document indexed, etc.)
- Update UI on events
- Show notifications for background tasks
- Test event flow end-to-end

**Deliverables:** Real-time notifications and progress updates

### Issue #27: Security Audit & Hardening
- **Time:** 2-3 hours
- **Link:** https://github.com/buddha314/babocument/issues/27

Input sanitization, CORS, rate limiting, file upload validation.

### Issue #23: Authentication & Authorization
- **Time:** 4-6 hours
- **Link:** https://github.com/buddha314/babocument/issues/23

JWT/API keys, middleware, protected endpoints.

### Issue #18: CI/CD Pipeline
- **Time:** 2-3 hours
- **Link:** https://github.com/buddha314/babocument/issues/18

GitHub Actions for server + client testing.

### Issue #20: Database Layer
- **Time:** 3-4 hours
- **Link:** https://github.com/buddha314/babocument/issues/20

SQLAlchemy models, migrations, persistent metadata.

---

## P2 - MEDIUM (Quality Improvements & Advanced Features)

### Issue #35: 3D Timeline Visualization (Client) ⭐ **NEW**
- **Time:** 12-16 hours
- **Status:** Not started
- **Depends on:** #32
- **Link:** TBD

Integrate API data with BabylonJS 3D timeline corridor.

**Tasks:**
- Create Timeline3D component
- Generate document meshes from API data
- Sort documents by year in 3D space
- Add interactive document selection
- Implement search result highlighting in 3D
- Optimize for VR/XR performance
- Add VR controller support

**Deliverables:** Immersive 3D document timeline

### Issue #36: Statistics Dashboard (Client) ⭐ **NEW**
- **Time:** 6-8 hours
- **Status:** Not started
- **Depends on:** #30
- **Link:** TBD

Create statistics dashboard showing system metrics and document analytics.

**Tasks:**
- Create stats API methods
- Create useStats hook
- Build StatsPanel component
- Build charts (document counts by year, source trends)
- Add real-time updates via WebSocket
- Display agent performance metrics

**Deliverables:** Interactive statistics dashboard

### Issue #37: Repository Management UI (Client) ⭐ **NEW**
- **Time:** 4-6 hours
- **Status:** Not started
- **Depends on:** #30
- **Link:** TBD

Create UI for managing document repositories and MCP server connections.

**Tasks:**
- Create repository API methods
- Create useRepositories hook
- Build RepositoryManager component
- Show connection status and health
- Add sync functionality
- Display repository document counts

**Deliverables:** Repository management interface

### Issue #21: WebSocket Handler (Server)
- **Time:** 2-3 hours
- **Depends on:** #19
- **Link:** https://github.com/buddha314/babocument/issues/21

Real-time updates for agent tasks.

### Issue #22: Background Task Processing
- **Time:** 2-3 hours
- **Depends on:** #19
- **Link:** https://github.com/buddha314/babocument/issues/22

Celery for async PDF processing.

### Issue #25: Error Handling Standardization
- **Time:** 2-3 hours
- **Link:** https://github.com/buddha314/babocument/issues/25

Consistent error responses across APIs.

### Issue #28: Resolve All TODOs
- **Time:** 2-3 hours
- **Link:** https://github.com/buddha314/babocument/issues/28

Clean up 19 TODO comments in codebase.

### Issue #24: API Documentation & Usage Guide
- **Time:** 2-3 hours
- **Link:** https://github.com/buddha314/babocument/issues/24

Create docs/API_USAGE_GUIDE.md with examples.

### Issue #14: Select Optimal LLM Models
- **Time:** Research + benchmarking
- **Link:** https://github.com/buddha314/babocument/issues/14

Benchmark models for each agent type.

---

## P3 - LOW (Future Work)

### Issue #31: TypeScript Type Definitions (Client) ⭐ **NEW**
- **Time:** 2-3 hours
- **Status:** Not started
- **Depends on:** #30
- **Link:** TBD

Generate or create TypeScript types for API communication.

**Options:**
1. Auto-generate from OpenAPI schema (recommended)
2. Manual type definitions

**Deliverables:** Type-safe API client

### Issue #29: Code Linting & Formatting
- **Time:** 1 hour
- **Link:** https://github.com/buddha314/babocument/issues/29

Black, flake8, mypy, pre-commit hooks.

### Issue #26: Documentation Cleanup
- **Time:** 1-2 hours
- **Link:** https://github.com/buddha314/babocument/issues/26

Consolidate SESSION_*.md files, remove duplicates.

### Issue #6: Plotly Integration Decision
- **Type:** Decision (Phase 3)
- **Link:** https://github.com/buddha314/babocument/issues/6

Canvas texture vs HTML overlay for 3D viz.

### Issue #7: Blender Asset Pipeline
- **Type:** Setup (Phase 3)
- **Link:** https://github.com/buddha314/babocument/issues/7

Blender → GLB export workflow.

### Issue #8: Keyword Trend Graphs
- **Type:** Feature (Phase 5)
- **Depends on:** #10
- **Link:** https://github.com/buddha314/babocument/issues/8

Plotly visualizations of keyword trends.

### Issue #11: Data Visualization UI
- **Type:** Epic (Phase 3)
- **Link:** https://github.com/buddha314/babocument/issues/11

Complete BabylonJS + Plotly integration.

---

## ✅ Completed

### Issue #19: Event Bus Implementation
- **Completed:** 2025-11-06
- Redis pub/sub with 6 event types
- 12 tests passing, integrated with API
- See HANDOFF_2025-11-06_EVENT_BUS.md

### Issue #15: Service Integration
- **Completed:** 2025-11-06
- 17 REST endpoints connected to Vector DB and LLM
- 92 tests passing, 84% coverage

### Issue #9: Vector DB Initialization
- **Completed:** 2025-11-06
- 4 papers indexed, semantic search working

### Issues #1-5: Phase 0 Decisions
- **Completed:** 2025-11-06
- All architectural decisions made

### Issue #12: Launch Scripts
- **Completed:** 2025-11-06
- PowerShell scripts for dev environment

---

## Quick Reference

**Total Issues:** 36 (26 open, 10 closed)

**Priority Distribution:**
- P0: 4 issues (18-26 hours) - 2 backend, 2 client
- P1: 8 issues (46-68 hours) - 4 backend, 4 client
- P2: 9 issues (36-54 hours) - 3 backend, 6 client
- P3: 7 issues (future)

**Time to Phase 1 (Backend):** 9-12 hours  
**Time to Phase 2 (Client Integration):** 32-46 hours (includes agent search)
**Time to Production:** 64-94 hours

**Next Action:** 
- **Backend:** Start Issue #10 (Agents)
- **Client:** Start Issue #30 (API Infrastructure)
- **Feature:** Issue #38 (Agent Paper Discovery) - After #10 and #32

---

For detailed dependency graph, risk assessment, and week-by-week plan, see:
**PRIORITY_ANALYSIS_2025-11-06.md**
