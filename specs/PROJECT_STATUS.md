# Project Status - Babocument

**Last Updated:** 2025-11-06
**Session:** Clean session initialization

## Project Overview

Babocument is an agentic VR/XR document management application for reviewing synthetic biology and biomanufacturing research documents. The system combines an immersive BabylonJS client experience with a FastAgent-powered multi-agent backend.

## Current State

### Repository Setup
- ✅ Git repository initialized
- ✅ .gitignore configured for Python, Node.js, and BabylonJS Editor
- ✅ Base directory structure in place

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
- MCP plugin for Godot
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

## Technical Decisions Pending

### High Priority
1. **Client-Server Communication Protocol**
   - Option A: WebSockets (real-time, bidirectional)
   - Option B: REST API with async (simpler, more standard)
   - Decision needed before backend implementation

2. **Agent Architecture Design**
   - Agent roles and responsibilities
   - Communication patterns
   - State management approach

3. **3D Asset Pipeline**
   - Asset creation workflow (Blender/Godot)
   - Import/export formats
   - Asset optimization strategy

### Medium Priority
4. **Authentication & Authorization**
   - User management system
   - Workspace permissions
   - Data access controls

5. **Database Selection**
   - Document storage
   - Metadata management
   - Search capabilities

6. **Deployment Strategy**
   - Development environment setup
   - Production hosting (client/server)
   - CI/CD pipeline

## Immediate Next Steps

### Before Next Session
- [ ] Define communication protocol (WebSockets vs REST)
- [ ] Design agent architecture
- [ ] Create technical specification docs

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
- Word clouds and trend analyses
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
