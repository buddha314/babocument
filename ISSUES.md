# GitHub Issues Index

**Repository:** https://github.com/buddha314/babocument/issues

**Last Updated:** 2025-11-06 (Synced with GitHub - Issues #1-3, #12 completed; #14 added)

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
**Status:** 🟡 Open | **Priority:** High | **Type:** Implementation

Create initialization script to populate vector database from data/papers directory

**Requirements:**
- Parse PDFs from `data/papers/`
- Extract full text and metadata
- Generate embeddings (Sentence Transformers or OpenAI)
- Configurable storage paths

**Script:** `server/scripts/init_vector_db.py`

**Phases:** 1 (setup), 2 (execution)

**Dependencies:** [#4](#issue-4-vector-database-selection)

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

**Total Issues:** 14

**Completed:** 6 (Issues #1, #2, #3, #4, #5, #12)

**By Type:**
- 🔷 Decisions: 7 (Issues #1-#6, #14) - 5 decided, 2 open
- 🔶 Setup: 1 (Issue #7)
- ⚙️ Features: 2 (Issues #8-#9)
- 📦 Epics: 2 (Issues #10-#11)
- 🛠️ DevOps: 1 (Issue #12) - completed

**By Priority:**
- 🔴 High: 12 (6 decided, 6 open)
- 🟡 Medium: 2

**By Phase:**
- Phase 0 (Planning): 7 decision issues (5 decided, 2 open)
- Phase 1 (Backend): 1 epic, 1 implementation
- Phase 2 (Data): 1 implementation
- Phase 3 (Frontend): 1 epic, 1 feature
- Phase 4 (Librarian): 0 (future)
- Phase 5 (Intelligence): 0 (future)
- Phase 6 (Management): 0 (future)

## Dependencies Graph

```
Phase 0 Decisions (#1, #2, #3 - DECIDED)
    ↓
Issue #14 (Select specific LLM models)
    ↓
Issue #10 (Phase 1: Backend Setup)
    ↓
Issue #9 (Initialize Vector DB)
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
