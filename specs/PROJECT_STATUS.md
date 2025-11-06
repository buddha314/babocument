# Project Status - Babocument

**Last Updated:** 2025-11-06 (Issue #4 Vector Database Decision)
**Session:** Phase 0 architectural decisions

## Project Overview

Babocument is an agentic VR/XR document management application for reviewing synthetic biology and biomanufacturing research documents. The system combines an immersive BabylonJS client experience with a FastAgent-powered multi-agent backend.

## Current State

### Repository Setup
- ✅ Git repository initialized
- ✅ .gitignore configured for Python, Node.js, and BabylonJS Editor
- ✅ Base directory structure in place

### Phase 0: Foundation & Planning Decisions

**Completed (3/7):**
- ✅ **Issue #4** - Vector Database Selection (ChromaDB)
- ✅ **Issue #5** - MCP Integration Strategy (Hybrid community servers)
- ✅ **Issue #12** - Launch Script (DevOps)

**In Progress (4/7):**
- 🟡 **Issue #1** - Communication Protocol (WebSockets vs REST)
- 🟡 **Issue #2** - Multi-Agent Architecture Design
- 🟡 **Issue #3** - LLM Hosting Solution
- 🟡 **Issue #6** - Plotly.js Integration Strategy
- 🟡 **Issue #7** - Blender Asset Pipeline

### Client Layer (/client)
**Status:** Scaffolded - BabylonJS Editor + Next.js template

**Technology Stack:**
- Next.js 14.2.32 (React 18)
- BabylonJS Core 8.33.2
- BabylonJS GUI 8.33.2
- BabylonJS Havok 1.3.10 (Physics)
- BabylonJS Materials 8.33.2
- BabylonJS Editor Tools (latest)
- TypeScript 5.8.3
- Tailwind CSS 3.3.0
- Plotly.js (planned - 3D scientific visualization)

**Current Structure:**
```
client/
├── .bjseditor/          # BabylonJS Editor project files
├── assets/              # Static assets and resources
├── public/              # Next.js public files
├── src/
│   ├── app/
│   │   ├── layout.tsx   # Next.js layout
│   │   └── page.tsx     # Main page
│   ├── scripts/
│   │   └── box.ts       # BabylonJS scene script
│   └── scripts.ts       # Script loader
├── package.json         # Dependencies
├── tsconfig.json        # TypeScript config
└── project.bjseditor    # Editor project file
```

**Implementation Status:**
- 🟡 Basic Next.js app structure
- 🟡 BabylonJS Editor integration template
- 🔴 Virtual environment (File Room) - Not started
- 🔴 Librarian character animation - Not started
- 🔴 UI components - Not started
- 🔴 Timeline visualization - Not started

### Server Layer (/server)
**Status:** Empty directory - Not started

**Planned Technology:**
- FastAgent API framework
- Multi-agent coordination system
- MCP (Model Context Protocol) integrations

**Implementation Status:**
- 🔴 FastAgent setup - Not started
- 🔴 Agent architecture - Not started
- 🔴 API endpoints - Not started
- 🔴 Data source integrations - Not started

### Integration Layer
**Status:** Not started

**Components:**
- MCP plugin for Blender
- BabylonJS Editor integration
- Client-Server communication (WebSockets vs REST+async TBD)

### Documentation (/specs)
**Status:** In progress

**Files Created:**
- PROJECT_STATUS.md (this file)
- Additional docs pending

### Data (/data)
**Present Directories:**
- lookbook/ - Visual style references
- papers/ - Research documents

## Technical Decisions

### Completed Decisions ✅

1. **MCP Integration for Document Repositories** ✅ DECIDED (2025-11-06)
   - **Decision:** Hybrid approach using community MCP servers
   - **Primary Sources:**
     - BioMCP (PubMed + ClinicalTrials.gov + MyVariant.info)
     - arXiv API MCP with LaTeX support
     - bioRxiv/medRxiv MCP servers
   - **Documentation:** [MCP_INTEGRATION_DECISION.md](MCP_INTEGRATION_DECISION.md)
   - **Next Step:** Begin Phase 1 implementation (Week 1-2)

2. **Vector Database Selection** ✅ DECIDED (2025-11-06)
   - **Decision:** Use **ChromaDB** with **Sentence Transformers** (all-MiniLM-L6-v2)
   - **Rationale:**
     - Simplest setup (pip install, no separate server)
     - Python-native (perfect for FastAgent backend)
     - Configurable local storage paths
     - Free and open source
     - Sufficient for 100k+ documents
   - **Embedding Model:** all-MiniLM-L6-v2 (384 dimensions, ~3000 sentences/sec)
   - **Documentation:** [VECTOR_DATABASE_DECISION.md](VECTOR_DATABASE_DECISION.md)
   - **Next Step:** Install ChromaDB and implement VectorDatabase wrapper class

3. **Launch Script** ✅ COMPLETED (2025-11-06)
   - **Implementation:** PowerShell launch script with full dependency management
   - **File:** `launch.ps1`
   - **Features:** Background job management, auto-detection, graceful shutdown
   - **Usage:** `.\launch.ps1 -ClientOnly` (current phase)

### Pending Decisions 🟡

1. **Client-Server Communication Protocol**
   - Option A: WebSockets (real-time, bidirectional)
   - Option B: REST API with async (simpler, more standard)
   - Decision needed before backend implementation

2. **Agent Architecture Design**
   - Agent roles and responsibilities
   - Communication patterns
   - State management approach

3. **3D Asset Pipeline**
   - Asset creation workflow (Blender → BabylonJS)
   - Import/export formats (GLB via GLTF 2.0)
   - Asset optimization strategy

### Medium Priority
6. **Authentication & Authorization**
   - User management system
   - Workspace permissions
   - Data access controls

7. **Database Selection**
   - Document storage (traditional DB)
   - Metadata management
   - Workspace persistence

6. **Deployment Strategy**
   - Development environment setup
   - Production hosting (client/server)
   - CI/CD pipeline

## Immediate Next Steps

### Phase 0: DevOps & Setup (NEW - Critical Priority) ⭐
- [ ] Create unified launch script - [Issue #12](https://github.com/buddha314/babocument/issues/12) - **CRITICAL**
  - PowerShell script for Windows development
  - Start server and client with single command
  - Environment validation and dependency checks
  - Supports `--client-only` flag for current work

### Phase 0 Decisions
- [ ] Define communication protocol (WebSockets vs REST) - [Issue #1](https://github.com/buddha314/babocument/issues/1)
- [ ] Design agent architecture - [Issue #2](https://github.com/buddha314/babocument/issues/2)
- [ ] Choose LLM hosting solution - [Issue #3](https://github.com/buddha314/babocument/issues/3)
- [x] Select vector database - [Issue #4](https://github.com/buddha314/babocument/issues/4) ✅ COMPLETED (ChromaDB)
- [x] Plan MCP integration - [Issue #5](https://github.com/buddha314/babocument/issues/5) ✅ COMPLETED (Hybrid community servers)
- [ ] Decide Plotly integration - [Issue #6](https://github.com/buddha314/babocument/issues/6)
- [ ] Set up Blender pipeline - [Issue #7](https://github.com/buddha314/babocument/issues/7)

### MCP Integration (Phase 1 - Ready to Start)
- [ ] Install and test BioMCP server
- [ ] Install and test arXiv MCP server
- [ ] Install and test bioRxiv/medRxiv MCP server
- [ ] Create unified Research Agent interface
- [ ] Integrate with vector database (pending Issue #4)
- [ ] Build API endpoints for paper search

### Client Development
- [ ] Design File Room virtual environment layout
- [ ] Create Librarian character model/animation pipeline
- [ ] Implement basic BabylonJS scene with timeline corridor
- [ ] Build UI component library

### Server Development
- [ ] Set up FastAgent project structure
- [ ] Define API endpoints
- [ ] Implement agent coordinator
- [ ] Integrate data sources (journals, ClinicalTrials.gov)

## Key User Features (Target)

### Research & Discovery
- Query bioinks and academic journals with timeline visualization
- Timeline-sorted journal articles
- Word clouds and keyword trend line graphs
- Temporal trend analysis across research corpus
- ClinicalTrials.gov correlation

### Document Management
- Open articles and explore embedded ideas
- Create and manage research workspaces
- View workspace associations
- Save and analyze article summaries

### Interactive Experience
- Virtual "file room" descending through time
- Glass-paned year partitions
- Virtual labs for collaboration
- Video upload with text/image extraction
- 3D laboratory equipment models

## Primary User Persona

**Beabadoo** - Computational Research Scientist
- Background: Graduate degree in computational chemistry
- Role: Supports researchers in biomanufacturing at synthetic biology corp
- Tasks: Bioinformatics, computational drug discovery models
- Expertise: Chemistry, biology, biomanufacturing, mathematics

## Notes

- Client uses BabylonJS Editor project format (.bjseditor)
- Visual style references located in data/lookbook/
- Server directory is completely empty - needs full implementation
- No git commits made yet - fresh initialization
