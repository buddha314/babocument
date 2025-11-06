# Babocument

> An immersive VR/XR document management platform for synthetic biology and biomanufacturing research

Babocument combines cutting-edge 3D visualization with AI-powered research assistance to transform how computational scientists interact with academic literature. Navigate through time in a virtual file room, guided by an intelligent Librarian character, while multi-agent systems help you discover insights across thousands of research papers.

## Quick Start

### Automated Launch (Recommended)

Use the unified launch script to start both client and server with automatic dependency management:

```powershell
# Launch both server and client (when server is implemented)
.\launch.ps1

# Launch only the client (current phase - server not yet implemented)
.\launch.ps1 -ClientOnly

# Launch without dependency checks
.\launch.ps1 -NoInstall

# Custom ports
.\launch.ps1 -ClientPort 3001 -ServerPort 8001
```

The launch script will:
- ✓ Validate Node.js, npm, and Python installations
- ✓ Check and install dependencies automatically
- ✓ Start services on configurable ports
- ✓ Handle graceful shutdown with Ctrl+C

**Current Status:** Server is not yet implemented (Phase 1). Use `-ClientOnly` flag or the script will automatically detect and launch client only.

### Manual Launch

#### Client (BabylonJS + Next.js)
```bash
cd client
npm install
npm run dev
```
Visit [http://localhost:3000](http://localhost:3000)

#### Server (FastAgent - Coming Soon)
```bash
cd server
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m fastagent.app
```

### Documentation
See [specs/](specs/) for detailed project documentation:
- [Project Status](specs/PROJECT_STATUS.md) - Current implementation state
- [Task Tracking](specs/TASKS.md) - Development roadmap and task lists

## Architecture

### Core Components

**Client Layer** ([/client](client/))
- BabylonJS 8.33.2 with Havok physics engine
- Next.js 14 + React 18 + TypeScript
- Animated Librarian character guide
- Immersive timeline-based file room
- VR/XR support

**Server Layer** ([/server](server/)) - *In Planning*
- FastAgent API framework
- Multi-agent coordination system
- Research data aggregation
- Real-time analysis and recommendations

**Integration Layer** - *Planned*
- MCP (Model Context Protocol) plugins
- Blender integration for 3D assets
- BabylonJS Editor for scene composition

**Communication** - *Decision Pending*
- Option A: WebSockets (real-time, bidirectional)
- Option B: REST API with async (simpler, more standard)

## Primary User Persona

### Beabadoo - Computational Research Scientist

Beabadoo is a computational researcher in biomanufacturing at a major synthetic biology corporation.

**Background:**
- Graduate degree in computational chemistry
- Works at intersection of chemistry, biology, and biomanufacturing
- Strong mathematics and computational modeling skills

**Daily Tasks:**
- Supporting lab researchers with computational analyses
- Bioinformatics and data pipeline work
- Computational drug discovery modeling
- Literature review and trend analysis

**Pain Points:**
- Information overload from multiple journal sources
- Difficulty tracking research evolution over time
- Lack of intuitive visualization for research trends
- Isolated document review without spatial context

## Key Features

### Research & Discovery
- Query bioinks and academic journals with timeline visualization
- Access sorted journal articles by publication year
- Generate word clouds and keyword trend line graphs of research over time
- Track keyword frequency and evolution across temporal corpus
- Search and correlate ClinicalTrials.gov data with current research
- **Discover and manage journal repositories** - Add new sources as you find them
- **Organize repositories into workspaces** - Different source sets for different projects

### Document Management
- Open articles and explore embedded research ideas
- Create and manage research workspaces
- **Collect journal repositories into workspace-specific collections**
- View workspace associations and relationships
- Save and analyze article summaries for pattern detection
- **Configure repository-scoped searches** per workspace

### Interactive Experience
- Navigate a virtual "file room" descending through time
- Glass-partitioned years create clear temporal boundaries
- Enter virtual labs for collaborative research sessions
- Upload videos for text and image extraction
- View and interact with 3D models of laboratory equipment

### Data Sources
- Public journal repositories (configurable list)
- Web search for scientific topics
- Full-text academic articles (arXiv, PubMed, etc.)
- ClinicalTrials.gov API integration

## Virtual Environment Design

### File Room
A continuous hallway descending through time, where users walk through the evolution of research. Glass partitions separate different publication years, creating a physical timeline that can be explored intuitively.

### Virtual Labs
Collaborative spaces designed for team research sessions, featuring 3D models of biomanufacturing equipment and tools.

### Visual Style
Inspired by curated references in [./data/lookbook](data/lookbook/):
- Clean, scientific aesthetic
- Modern UI with minimal chrome
- Smooth animations and transitions
- Responsive across desktop, VR, and XR devices

## Multi-Agent System

The backend employs specialized AI agents working in concert:

**Research Agent** - Query understanding and multi-source search
**Analysis Agent** - Trend detection, word clouds, correlations
**Summary Agent** - Article summarization and key insights
**Recommendation Agent** - Related paper suggestions and gap identification
**Coordination Agent** - Orchestrates agent collaboration

## Technology Stack

**Frontend:**
- BabylonJS 8.33.2 (3D engine)
- Next.js 14.2.32 (React framework)
- TypeScript 5.8.3
- Tailwind CSS 3.3.0
- Plotly.js (scientific visualization, 3D plots)

**Backend:** *(Planned)*
- FastAgent (Python)
- Multi-agent framework
- Data integration APIs

**Tools:**
- BabylonJS Editor (scene creation)
- Blender (3D modeling and GLB export)

## Project Status

**Phase:** Foundation & Planning
**Last Updated:** 2025-11-06

**Completed:**
- ✅ Git repository initialization
- ✅ Project structure and configuration
- ✅ Client scaffolding with BabylonJS Editor
- ✅ Documentation framework

**In Progress:**
- 🟡 Technical architecture decisions
- 🟡 API design and specifications

**Next Steps:**
- Communication protocol decision (WebSockets vs REST) - [Issue #1](https://github.com/buddha314/babocument/issues/1)
- Multi-agent architecture design - [Issue #2](https://github.com/buddha314/babocument/issues/2)
- Vector database selection - [Issue #4](https://github.com/buddha314/babocument/issues/4)
- ✅ **MCP integration strategy** - [Issue #5](https://github.com/buddha314/babocument/issues/5) - **DECIDED: Hybrid approach with BioMCP, arXiv, and bioRxiv community servers**
- Server implementation kickoff - [Issue #10](https://github.com/buddha314/babocument/issues/10)

See [specs/PROJECT_STATUS.md](specs/PROJECT_STATUS.md) for detailed status and [specs/TASKS.md](specs/TASKS.md) for the complete roadmap.

## Contributing

This project is in active development. Check [specs/TASKS.md](specs/TASKS.md) for current priorities.

## License

*License TBD*