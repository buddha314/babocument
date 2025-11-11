# Specifications & Documentation Index

**Babocument Server Documentation**  
**Last Updated:** November 11, 2025

## Quick Navigation

### 🎯 Essential Reading
- **Architecture**: `MULTI_AGENT_ARCHITECTURE.md` - Agent system design
- **Project Status**: `PROJECT_STATUS.md` - Current state and roadmap
- **Tasks**: `TASKS.md` - Development tasks and priorities

### 🔧 Technical Specifications
- **Vector Database**: `VECTOR_DATABASE_SPEC.md` & `VECTOR_DATABASE_DECISION.md`
- **LLM Integration**: `LLM_HOSTING_DECISION.md`
- **MCP Integration**: `MCP_INTEGRATION_SPEC.md` & `MCP_INTEGRATION_DECISION.md`
- **Communication**: `COMMUNICATION_PROTOCOL_DECISION.md`

### 📋 Historical Context
- **Handoffs**: `HANDOFF_*.md` - Development session summaries
- **Repository Split**: `REPOSITORY_SPLIT_DOCUMENTATION.md`
- **Issues**: `ISSUES.md` & `GITHUB_ISSUES_TO_CREATE.md`

---

## Document Categories

### Architecture & Design

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
- `TASKS.md` - Current development tasks and priorities
- `GITHUB_ISSUES_TO_CREATE.md` - Planned GitHub issues
- `ISSUES.md` - Issue tracking and categorization

**Historical:**
- `TASKS_OLD.md` - Previous task list (archived)
- `TASKS_OLD_DETAILED.md` - Detailed old tasks (archived)
- `ISSUES_OLD.md` - Old issue tracking (archived)

### Feature Specifications

**User Stories:**
- `USER_STORY_AGENT_PAPER_DISCOVERY.md` - Agent-assisted search feature
- `USER_STORY_DICOM_VISUALIZATION.md` - Medical imaging support (future)

**Client Integration** (Historical - now in Godot repo):
- `CLIENT_AGENT_FIRST_REDESIGN.md` - Conversational UI paradigm
- `CLIENT_API_INTEGRATION_PLAN.md` - API client architecture
- `BLENDER_INTEGRATION_PLAN.md` - 3D asset pipeline (BabylonJS era)
- `WEBXR_IMPLEMENTATION_GUIDE.txt` - WebXR setup (BabylonJS era)
- `GITHUB_ISSUE_46_VR_CHAT.md` - VR chat implementation (BabylonJS era)
- `VISUALIZATION_REQUIREMENTS.md` - Data viz requirements

### Utilities & Notes

**Development Tools:**
- `HOW_TO_CREATE_ISSUES.md` - Issue creation guide
- `ISSUE_12_LAUNCH_SCRIPT.md` - Launch script notes
- `NETWORK_ACCESS.md` - Network configuration notes

---

## Document Status

### ✅ Current & Maintained
- Architecture specifications
- Task lists
- Project status
- Handoff documents (latest)

### 📦 Archived (Historical Reference)
- Old task lists
- Old issues
- Previous client integration docs (BabylonJS/Unity)
- Development utility guides

### 🔄 Client-Specific (Move to Godot Repo)
- BabylonJS integration plans
- WebXR guides  
- Unity-specific docs
- 3D visualization requirements

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
