# Specifications & Documentation Index

**Babocument Server Documentation**  
**Last Updated:** November 11, 2025

## Quick Navigation

### 🎯 Essential Reading (Start Here)
- **Architecture**: `MULTI_AGENT_ARCHITECTURE.md` - Agent system design
- **Project Status**: `PROJECT_STATUS.md` - Current state (✅ Production Ready)
- **Tasks**: `TASKS.md` - Active development tasks and priorities
- **Agent Design**: `CLIENT_AGENT_FIRST_REDESIGN.md` - Conversational interface paradigm

### 🔧 Technical Specifications
- **Vector Database**: `VECTOR_DATABASE_SPEC.md` & `VECTOR_DATABASE_DECISION.md`
- **LLM Integration**: `LLM_HOSTING_DECISION.md`
- **MCP Integration**: `MCP_INTEGRATION_SPEC.md` & `MCP_INTEGRATION_DECISION.md`
- **Communication**: `COMMUNICATION_PROTOCOL_DECISION.md`

### 📋 Development History
- **Recent Handoffs**: `HANDOFF_2025-11-07_*.md` - Recent development sessions
- **Repository Split**: `REPOSITORY_SPLIT_DOCUMENTATION.md` - Monorepo → separate repos
- **Archived Tasks**: `TASKS_CLIENT_BABYLONJS.old` - Previous BabylonJS-focused tasks

---

## Document Categories

### Current & Active

**Core Architecture:**
- `MULTI_AGENT_ARCHITECTURE.md` - Multi-agent system design
- `COMMUNICATION_PROTOCOL_DECISION.md` - REST + WebSocket architecture
- `PROJECT_STATUS.md` - Current implementation status

**Data & AI:**
- `VECTOR_DATABASE_SPEC.md` - ChromaDB implementation details
- `VECTOR_DATABASE_DECISION.md` - Vector DB selection rationale
- `LLM_HOSTING_DECISION.md` - Ollama + LiteLLM setup
- `MCP_INTEGRATION_SPEC.md` - Model Context Protocol integration
- `MCP_INTEGRATION_DECISION.md` - MCP strategy decisions

### Development History

**Handoff Documents** (chronological):
- `HANDOFF_FINAL_2025-11-06_VR_CHAT.md` - VR chat interface work (pre-split)
- `HANDOFF_2025-11-07_REPO_SPLIT.md` - Repository restructuring
- `HANDOFF_2025-11-07_AGENT_ENDPOINT.md` - Agent API implementation
- `HANDOFF_2025-11-07_AGENT_CHAT_WORKING.md` - LLM integration completion

**Repository Organization:**
- `REPOSITORY_SPLIT_DOCUMENTATION.md` - Documentation distribution guide

### Task Management

**Active:**
- `TASKS.md` - Current development tasks and priorities (server-focused, updated Nov 11)

**Archived:**
- `TASKS_CLIENT_BABYLONJS.old` - Previous BabylonJS-focused tasks (archived Nov 11)
- `GITHUB_ISSUES_BABYLONJS.old` - BabylonJS-focused GitHub issues (archived Nov 11)
- `ISSUES_BABYLONJS.old` - BabylonJS-focused issue tracker (archived Nov 11)

### Feature Specifications

**Active User Stories:**
- `USER_STORY_AGENT_PAPER_DISCOVERY.md` - Agent-assisted search feature

**Client Integration Paradigms:**
- `CLIENT_AGENT_FIRST_REDESIGN.md` - Conversational UI paradigm (applies to all clients)

**Note:** Client-specific implementation docs (BabylonJS, Unity, WebXR) have been removed as the primary client is now [beabodocl-godot](https://github.com/buddha314/beabodocl-godot).

---

## Document Status

### ✅ Current & Maintained
- Architecture specifications (MULTI_AGENT_ARCHITECTURE.md, etc.)
- Technical decisions (VECTOR_DATABASE_DECISION.md, LLM_HOSTING_DECISION.md, etc.)
- Current task list (TASKS.md - updated Nov 11)
- Project status (PROJECT_STATUS.md - updated Nov 11)
- Handoff documents (HANDOFF_2025-11-07_*.md)

### 📦 Archived (Historical Reference)
- TASKS_CLIENT_BABYLONJS.old - Previous BabylonJS-focused task list
- GITHUB_ISSUES_BABYLONJS.old - BabylonJS-focused issues
- ISSUES_BABYLONJS.old - BabylonJS-focused issue tracker

### 🗑️ Removed (Nov 11 cleanup)
- TASKS_OLD.md, TASKS_OLD_DETAILED.md, ISSUES_OLD.md - Completely obsolete task files
- BLENDER_INTEGRATION_PLAN.md, WEBXR_IMPLEMENTATION_GUIDE.txt - BabylonJS-specific
- GITHUB_ISSUE_46_VR_CHAT.md, CLIENT_API_INTEGRATION_PLAN.md - BabylonJS client plans
- USER_STORY_DICOM_VISUALIZATION.md, VISUALIZATION_REQUIREMENTS.md - Client-specific features
- NETWORK_ACCESS.md, HOW_TO_CREATE_ISSUES.md, ISSUE_12_LAUNCH_SCRIPT.md - Dev utility docs

---

## Using This Documentation

### For Developers

**Getting Started:**
1. Read `../README.md` - Server overview and quick start
2. Read `MULTI_AGENT_ARCHITECTURE.md` - Understand agent system
3. Read `TASKS.md` - See current development priorities

**Deep Dives:**
- Vector DB: Start with `VECTOR_DATABASE_DECISION.md`, then `VECTOR_DATABASE_SPEC.md`
- LLM Integration: Read `LLM_HOSTING_DECISION.md`
- API Design: Check `COMMUNICATION_PROTOCOL_DECISION.md`

**Historical Context:**
- Check `HANDOFF_*.md` files for development history
- Review `REPOSITORY_SPLIT_DOCUMENTATION.md` for org structure

### For Client Developers

**Primary Client:** [beabodocl-godot](https://github.com/buddha314/beabodocl-godot)

**Integration Docs:**
- `COMMUNICATION_PROTOCOL_DECISION.md` - API architecture
- `../README.md` - API endpoints overview
- Server API docs: http://localhost:8000/docs

**Shared Concepts:**
- `CLIENT_AGENT_FIRST_REDESIGN.md` - Conversational UI paradigm (applies to all clients)

---

## Maintenance

**When to Update:**
- Add new `HANDOFF_*.md` after major development sessions
- Update `PROJECT_STATUS.md` when milestones complete
- Update `TASKS.md` as priorities change
- Archive obsolete documents to keep specs/ organized

**Naming Conventions:**
- Architecture: `[TOPIC]_ARCHITECTURE.md`
- Decisions: `[TOPIC]_DECISION.md`
- Specifications: `[TOPIC]_SPEC.md`
- Handoffs: `HANDOFF_YYYY-MM-DD_[TOPIC].md`
- User Stories: `USER_STORY_[FEATURE].md`

---

**Index maintained by:** Development team  
**Last review:** November 11, 2025
