# Repository Split: Documentation & Issue Distribution

**Date:** November 7, 2025  
**Server Repo:** https://github.com/buddha314/babocument  
**Client Repo:** https://github.com/buddha314/beabodocl-babylon  
**Local Client Path:** `C:\Users\b\src\beabodocl-babylon`

## Overview

This document outlines which documentation files and GitHub issues belong to which repository after the monorepo split.

---

## 📦 Server Repository (babocument)

### Keep in Server Repo

**Core Documentation:**
- ✅ `README.md` - Updated with server-only focus + client link
- ✅ `SETUP.md` - Server environment setup
- ✅ `LICENSE` - MIT license (applies to both, but keep in server)
- ✅ `requirements.txt` - Python dependencies
- ✅ `pytest.ini` - Python test configuration
- ✅ `setup.ps1` - Server environment setup script

**Handoff Documents:**
- ✅ `HANDOFF_2025-11-07_REPO_SPLIT.md` - Repository restructuring
- ⚠️ `HANDOFF_FINAL_2025-11-06_VR_CHAT.md` - Keep (historical reference)

**Specifications (specs/):**
- ✅ `specs/MULTI_AGENT_ARCHITECTURE.md` - **SERVER** - Agent system design
- ✅ `specs/LLM_HOSTING_DECISION.md` - **SERVER** - Ollama/LiteLLM setup
- ✅ `specs/VECTOR_DATABASE_DECISION.md` - **SERVER** - ChromaDB selection
- ✅ `specs/VECTOR_DATABASE_SPEC.md` - **SERVER** - ChromaDB implementation
- ✅ `specs/MCP_INTEGRATION_DECISION.md` - **SERVER** - MCP server strategy
- ✅ `specs/MCP_INTEGRATION_SPEC.md` - **SERVER** - MCP implementation details
- ✅ `specs/COMMUNICATION_PROTOCOL_DECISION.md` - **SHARED** - Keep in server, reference in client
- ✅ `specs/PROJECT_STATUS.md` - **SERVER** - Update to reflect server-only status
- ⚠️ `specs/VISUALIZATION_REQUIREMENTS.md` - **SHARED** - Extract client parts to client repo
- ⚠️ `specs/TASKS.md` - **SPLIT** - Separate server vs client tasks
- 🗑️ `specs/TASKS_OLD_DETAILED.md` - Archive/delete (obsolete)

**Session Documentation (docs/sessions/):**
- ✅ `docs/sessions/SESSION_2025-11-06_MCP_DECISION.md` - **SERVER**
- ✅ `docs/sessions/SESSION_2025-11-06_PHASE1_INIT.md` - **SERVER**
- ✅ `docs/sessions/SESSION_2025-11-06_REST_API_IMPLEMENTATION.md` - **SERVER**
- ✅ `docs/sessions/SESSION_2025-11-06_REST_API_TESTS.md` - **SERVER**
- ✅ `docs/sessions/SESSION_2025-11-06_SERVER_CLEANUP.md` - **SERVER**
- ✅ `docs/sessions/SESSION_SUMMARY.md` - **SERVER**
- ✅ `docs/sessions/README.md` - **SERVER**
- 📦 `docs/sessions/VR_CHAT_INTERFACE_GUIDE.md` - **MOVE TO CLIENT**
- 📦 `docs/sessions/BABYLON_CLIENT_STRUCTURE.md` - **MOVE TO CLIENT**
- 📦 `docs/sessions/BABYLON_QUICK_REFERENCE.md` - **MOVE TO CLIENT**
- 📦 `docs/sessions/EXPLORATION_SUMMARY.md` - **MOVE TO CLIENT**
- 📦 `docs/sessions/PROJECT_ASSET_STRUCTURE.md` - **MOVE TO CLIENT**
- 📦 `docs/sessions/ASSET_DOCUMENTATION_INDEX.md` - **MOVE TO CLIENT**

**Other Docs:**
- 🗑️ `docs/BLENDER_WORKFLOW.md` - **MOVE TO CLIENT**
- 🗑️ `docs/PLOTLY_BABYLONJS_INTEGRATION.md` - **MOVE TO CLIENT**

**Scripts:**
- ✅ `SCRIPTS.md` - **SERVER** - Update for server-only scripts
- ✅ `start-dev.ps1` - **SERVER**
- ✅ `run-server.ps1` - **SERVER**
- 🗑️ Delete: `create-github-issues.ps1`, `create-issues-simple.ps1` (project specific utilities)

**Issues & Tasks:**
- ⚠️ `ISSUES.md` - **SPLIT** - Separate server vs client issues
- 🗑️ `ISSUES_OLD.md` - Archive/delete
- ⚠️ `GITHUB_ISSUES_TO_CREATE.md` - **SPLIT** - Separate server vs client
- 🗑️ `TASKS_OLD.md` - Archive/delete
- 🗑️ `HOW_TO_CREATE_ISSUES.md` - Archive/delete
- 🗑️ `ISSUE_12_LAUNCH_SCRIPT.md` - Archive/delete (obsolete)

**Design Documents:**
- ⚠️ `CLIENT_AGENT_FIRST_REDESIGN.md` - **SHARED/CLIENT** - Agent interface decisions affect both
- 📦 `CLIENT_API_INTEGRATION_PLAN.md` - **MOVE TO CLIENT**
- 📦 `BLENDER_INTEGRATION_PLAN.md` - **MOVE TO CLIENT**
- 📦 `WEBXR_IMPLEMENTATION_GUIDE.txt` - **MOVE TO CLIENT**
- ⚠️ `USER_STORY_AGENT_PAPER_DISCOVERY.md` - **SHARED** - Keep summary in server, full in client
- 📦 `USER_STORY_DICOM_VISUALIZATION.md` - **MOVE TO CLIENT**
- 📦 `GITHUB_ISSUE_46_VR_CHAT.md` - **MOVE TO CLIENT**
- 🗑️ `NETWORK_ACCESS.md` - Archive/delete (development notes)

---

## 🎨 Client Repository (beabodocl-babylon)

### Move to Client Repo

**Documentation to Move:**
- 📦 `docs/BLENDER_WORKFLOW.md` - 3D asset pipeline
- 📦 `docs/PLOTLY_BABYLONJS_INTEGRATION.md` - Visualization integration
- 📦 `docs/sessions/VR_CHAT_INTERFACE_GUIDE.md` - VR chat implementation
- 📦 `docs/sessions/BABYLON_CLIENT_STRUCTURE.md` - BabylonJS structure
- 📦 `docs/sessions/BABYLON_QUICK_REFERENCE.md` - BabylonJS reference
- 📦 `docs/sessions/EXPLORATION_SUMMARY.md` - Frontend exploration
- 📦 `docs/sessions/PROJECT_ASSET_STRUCTURE.md` - Asset structure
- 📦 `docs/sessions/ASSET_DOCUMENTATION_INDEX.md` - Asset index

**Design Documents:**
- 📦 `CLIENT_API_INTEGRATION_PLAN.md` - API client architecture
- 📦 `BLENDER_INTEGRATION_PLAN.md` - 3D workflow
- 📦 `WEBXR_IMPLEMENTATION_GUIDE.txt` - WebXR setup
- 📦 `USER_STORY_DICOM_VISUALIZATION.md` - DICOM viewer feature
- 📦 `GITHUB_ISSUE_46_VR_CHAT.md` - VR chat interface issue

**Shared Documents (Extract Client Parts):**
- 📝 Extract from `specs/VISUALIZATION_REQUIREMENTS.md` - Plotly/3D viz requirements
- 📝 Extract from `CLIENT_AGENT_FIRST_REDESIGN.md` - Frontend/UI parts
- 📝 Extract from `USER_STORY_AGENT_PAPER_DISCOVERY.md` - Frontend UI parts

**New Documents to Create in Client:**
- 🆕 `README.md` - Client setup and development
- 🆕 `CONTRIBUTING.md` - Client contribution guidelines
- 🆕 `SETUP.md` - Frontend environment setup
- 🆕 `ARCHITECTURE.md` - BabylonJS + Next.js architecture
- 🆕 `API_CLIENT_GUIDE.md` - How to integrate with server API

---

## 📋 GitHub Issues Distribution

### Server Repository Issues (babocument)

**Backend/Infrastructure:**
- ✅ Issue #19: Event Bus Implementation ✅ **COMPLETE**
- ✅ Issue #10: Complete Agents ✅ **COMPLETE**
- ✅ Issue #15: REST API Endpoints ✅ **COMPLETE**
- ✅ Issue #9: Vector DB Initialization ✅ **COMPLETE**
- ⚠️ Issue #20: Database Layer for Metadata **KEEP**
- ⚠️ Issue #21: WebSocket Handler **KEEP**
- ⚠️ Issue #22: Background Task Processing **KEEP**
- ⚠️ Issue #23: Authentication & Authorization **KEEP**
- ⚠️ Issue #24: API Documentation & Usage Guide **KEEP**
- ⚠️ Issue #25: Error Handling Standardization **KEEP**
- ⚠️ Issue #27: Security Audit & Hardening **KEEP**
- ⚠️ Issue #28: Resolve All TODOs **KEEP**
- ⚠️ Issue #18: CI/CD Pipeline **SPLIT** - Server and client pipelines

**Agent System:**
- ⚠️ Issue #38: Agent-Assisted Paper Discovery **SPLIT** - Backend stays, frontend moves
- ⚠️ Issue #40: Conversational Agent Interface **SPLIT** - Backend stays, frontend moves
- ⚠️ Issue #44: Workspace Management via Conversation **SPLIT** - Backend stays, frontend moves
- ⚠️ Issue #45: Proactive Agent Behaviors **KEEP** - Mostly backend

**LLM & Data:**
- ⚠️ Issue #14: Select Optimal LLM Models **KEEP**
- ✅ Issue #1-5: Phase 0 Decisions ✅ **COMPLETE**

### Client Repository Issues (beabodocl-babylon)

**Frontend/VR:**
- 📦 Issue #30: Client API Infrastructure Setup **MOVE**
- 📦 Issue #31: TypeScript Type Definitions **MOVE**
- 📦 Issue #32: Document API Integration **MOVE**
- 📦 Issue #33: Search Integration **MOVE**
- 📦 Issue #34: WebSocket Real-time Updates **MOVE**
- 📦 Issue #35: 3D Timeline Visualization **MOVE**
- 📦 Issue #36: Statistics Dashboard **MOVE**
- 📦 Issue #37: Repository Management UI **MOVE**
- 📦 Issue #41: Agent Avatar & Spatial Presence **MOVE**
- 📦 Issue #42: Ambient Context UI **MOVE**
- 📦 Issue #43: Voice Interaction System **MOVE**
- 📦 Issue #46: 3D Chat Screen & Immersive VR **MOVE**

**Visualization:**
- 📦 Issue #6: Plotly.js Integration Decision **MOVE**
- 📦 Issue #7: Blender Asset Pipeline **MOVE**
- 📦 Issue #8: Keyword Trend Graphs **MOVE**
- 📦 Issue #11: Data Visualization UI **MOVE**
- 📦 Issue #39: DICOM Medical Imaging Support **MOVE**

**Misc Client:**
- 📦 Issue #26: Documentation Cleanup **SPLIT** - Each repo cleans own docs
- 📦 Issue #29: Code Linting & Formatting **SPLIT** - Separate configs

---

## 🔄 Shared/Split Items

### Items Requiring Splitting

**1. specs/TASKS.md**
- **Server Part:** Backend tasks, agents, APIs, database
- **Client Part:** Frontend tasks, UI components, 3D scenes, VR

**2. specs/VISUALIZATION_REQUIREMENTS.md**
- **Server Part:** Data APIs, statistics endpoints
- **Client Part:** Plotly integration, 3D rendering, VR UI

**3. CLIENT_AGENT_FIRST_REDESIGN.md**
- **Keep in Both:** Reference document showing architecture
- **Server Focus:** Conversational backend, agent logic
- **Client Focus:** Chat UI, spatial UI, voice I/O

**4. ISSUES.md & GITHUB_ISSUES_TO_CREATE.md**
- Split by backend vs frontend concerns
- Some issues (like #38, #40) need backend + frontend parts

### Cross-Repository References

**Server README should reference:**
- Client repository link ✅ (done)
- API documentation location
- WebSocket endpoint documentation

**Client README should reference:**
- Server repository link
- API endpoint documentation
- Server setup requirements (for local development)

---

## 🗑️ Files to Archive/Delete

**From Server Repo:**
- `ISSUES_OLD.md` - Obsolete
- `TASKS_OLD.md` - Obsolete
- `specs/TASKS_OLD_DETAILED.md` - Obsolete
- `HOW_TO_CREATE_ISSUES.md` - Project-specific utility
- `ISSUE_12_LAUNCH_SCRIPT.md` - Obsolete
- `NETWORK_ACCESS.md` - Development notes
- `create-github-issues.ps1` - Project-specific utility
- `create-issues-simple.ps1` - Project-specific utility
- `check-network.ps1` - Development utility

---

## 📝 Action Items

### Server Repository (babocument)

1. **Documentation Cleanup:**
   - [x] Update README.md with client link ✅
   - [ ] Update `specs/PROJECT_STATUS.md` to reflect server-only status
   - [ ] Update `specs/TASKS.md` - keep only server tasks
   - [ ] Archive obsolete .md files to `docs/archive/`
   - [ ] Update `SCRIPTS.md` to document server-only scripts

2. **Issue Management:**
   - [ ] Close completed issues on GitHub (#19, #10, #15, #9)
   - [ ] Update remaining issues to remove client-specific tasks
   - [ ] Create new server-specific issues as needed

3. **Code Documentation:**
   - [ ] Update API documentation at `/docs` endpoint
   - [ ] Document WebSocket endpoints
   - [ ] Create API usage guide for client developers

### Client Repository (beabodocl-babylon)

1. **Initial Setup:**
   - [ ] Create comprehensive README.md
   - [ ] Create SETUP.md with environment requirements
   - [ ] Create ARCHITECTURE.md documenting BabylonJS + Next.js structure
   - [ ] Create API_CLIENT_GUIDE.md for server integration

2. **Move Documentation:**
   - [ ] Copy client-specific docs from babocument repo
   - [ ] Create `docs/` directory structure
   - [ ] Move VR/BabylonJS session docs
   - [ ] Move Blender/Plotly integration docs

3. **Issue Management:**
   - [ ] Create GitHub issues for frontend work
   - [ ] Reference server issues where integration needed
   - [ ] Set up issue templates for client features

4. **Extract from Shared Docs:**
   - [ ] Extract visualization requirements relevant to frontend
   - [ ] Extract client tasks from TASKS.md
   - [ ] Extract frontend portions of agent-first redesign

---

## 🔗 Integration Points

### Server Exposes:

- REST API at `http://localhost:8000` (configurable)
- WebSocket at `ws://localhost:8000/ws/agent/{session_id}`
- API documentation at `http://localhost:8000/docs`
- OpenAPI spec at `http://localhost:8000/openapi.json`

### Client Consumes:

- All REST endpoints for CRUD operations
- WebSocket for real-time agent chat
- Static file serving (if needed)
- CORS configured for local development

### Shared Concepts:

- Agent conversational interface paradigm
- Document data models (TypeScript types from OpenAPI)
- Event types for real-time updates
- API versioning strategy (/api/v1/)

---

## 📊 Migration Checklist

### Phase 1: Documentation (In Progress)
- [x] Update server README with client link
- [x] Add local client path to server README
- [ ] Archive obsolete documentation
- [ ] Update specs/TASKS.md for server only
- [ ] Create REPOSITORY_SPLIT_DOCUMENTATION.md

### Phase 2: Client Repository Setup
- [ ] Initialize client repo with proper structure
- [ ] Copy relevant documentation
- [ ] Create new client-specific docs
- [ ] Set up GitHub issues

### Phase 3: Issue Management
- [ ] Close completed server issues
- [ ] Update server issues (remove client tasks)
- [ ] Create client issues in new repo
- [ ] Link related issues across repos

### Phase 4: Cross-References
- [ ] Update all server docs to reference client repo
- [ ] Update all client docs to reference server repo
- [ ] Ensure API documentation is discoverable
- [ ] Create integration guides

---

## 📚 Reference

**Server Repository:** https://github.com/buddha314/babocument  
**Client Repository:** https://github.com/buddha314/beabodocl-babylon  
**Local Paths:**
- Server: `c:\Users\b\src\babocument`
- Client: `C:\Users\b\src\beabodocl-babylon`

**Key Documents:**
- Server Architecture: `specs/MULTI_AGENT_ARCHITECTURE.md`
- Client Architecture: (to be created in client repo)
- API Integration: (to be moved to client repo)
- Agent-First Design: `CLIENT_AGENT_FIRST_REDESIGN.md` (shared reference)

**Last Updated:** November 7, 2025
