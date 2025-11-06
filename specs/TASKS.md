# Task Tracking - Babocument

**Session Start:** 2025-11-06
**Status:** Planning Phase

## Critical Path Tasks

### Phase 0: Foundation & Planning (Current)
**Goal:** Establish technical foundation and make key architectural decisions

- [x] Initialize git repository
- [x] Create .gitignore for project stack
- [x] Document current project state
- [ ] **DECISION REQUIRED:** Choose client-server communication protocol
  - WebSockets vs REST API with async
  - Impact: Backend architecture, real-time capabilities
  - Blocking: Server implementation
- [ ] **DECISION REQUIRED:** Design multi-agent architecture
  - Agent roles and responsibilities
  - Communication patterns between agents
  - State management approach
  - Blocking: Server implementation
- [ ] Define API contract/specifications
- [ ] Create technical architecture document
- [ ] **Set up Blender asset pipeline**
  - Establish directory structure for `.blend` source files and `.glb` exports
  - Document GLTF 2.0 export workflow for BabylonJS
  - Update .gitignore for Blender files
  - See: BLENDER_INTEGRATION_PLAN.md for full details
- [ ] **DECISION REQUIRED:** Choose local LLM hosting solution
  - Ollama (local inference, easy setup)
  - HuggingFace (transformers library, model hub access)
  - LangGraph (agentic workflows, state management)
  - Impact: Agent intelligence capabilities, deployment complexity
  - Consider: Performance, model selection, integration with FastAgent
- [ ] **DECISION REQUIRED:** Plotly integration strategy for 3D visualization
  - Determine Plotly.js integration with BabylonJS
  - 3D plots rendered natively in BabylonJS scene vs HTML overlay
  - WebGL context sharing strategy
  - Impact: Visualization capabilities, performance, UX
  - Consider: Plotly 3D scatter/surface plots, texture mapping to meshes
- [ ] **DECISION REQUIRED:** MCP integration for document repositories
  - Review MCP servers for arXiv, PubMed, and other journal sources
  - Evaluate available MCP servers (community or build custom)
  - Determine which repositories to support (arXiv, PubMed, bioRxiv, etc.)
  - Design agent access patterns to MCP servers
  - Impact: Data source availability, agent capabilities, maintenance burden
  - Consider: API rate limits, full-text access, metadata richness
- [ ] **DECISION REQUIRED:** Vector database selection and configuration
  - Choose vector DB: Chroma, Weaviate, Qdrant, Pinecone, or Milvus
  - Design configurable local paths for dev environments
  - Plan embedding strategy (OpenAI, local models, etc.)
  - Define initialization process for data/papers corpus
  - Impact: Search performance, semantic search quality, deployment complexity
  - Consider: Local-first development, embedding costs, scalability

### Phase 1: Server Foundation
**Goal:** Set up FastAgent backend with basic agent coordination

**Prerequisites:** Phase 0 decisions complete

- [ ] Initialize Python project structure in /server
- [ ] Set up FastAgent framework
- [ ] Implement agent coordinator/orchestrator
- [ ] Create base agent classes
- [ ] Define API endpoints (REST or WebSocket handlers)
- [ ] Set up development environment configuration
- [ ] Implement basic logging and monitoring
- [ ] Configure vector database integration
  - Install chosen vector DB (Chroma/Weaviate/Qdrant/etc.)
  - Create configurable storage paths for local dev
  - Set up embedding pipeline
  - Define collection/index schema for documents
  - Create initialization script for data/papers ingestion

**Estimated Timeline:** 1-2 weeks

### Phase 2: Data Source Integration
**Goal:** Connect to external research data sources

**Prerequisites:** Phase 1 complete

- [ ] Set up MCP server integrations for document repositories
  - Evaluate and select MCP servers (arXiv, PubMed, bioRxiv)
  - Configure MCP server connections
  - Expose MCP tools to Research Agent
  - Test full-text retrieval and metadata extraction
- [ ] Implement journal repository integrations
  - arXiv API integration (via MCP or direct)
  - PubMed/PubMed Central integration
  - bioRxiv for preprints
  - Additional sources from editable list
- [ ] Implement ClinicalTrials.gov API integration
- [ ] Create web search capability for scientific topics
- [ ] Build data normalization/transformation layer
- [ ] Implement caching strategy for API responses
- [ ] Add rate limiting and error handling
- [ ] Initialize vector database with local papers
  - Parse PDFs from data/papers directory
  - Extract text and metadata
  - Generate embeddings
  - Store in vector database for semantic search

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
  - Multi-source search coordination
  - Result ranking and relevance
- [ ] Analysis Agent
  - Trend analysis over time
  - Word cloud generation
  - Keyword trend line graphs (temporal visualization)
  - Correlation detection
- [ ] Summary Agent
  - Article summarization
  - Key insight extraction
  - Workspace summary generation
- [ ] Recommendation Agent
  - Related paper suggestions
  - Research direction recommendations
  - Gap identification

**Estimated Timeline:** 3-4 weeks

### Phase 6: Document Management
**Goal:** Workspace and document interaction features

**Prerequisites:** Phase 3, Phase 5 partially complete

- [ ] Workspace system
  - Create workspace API
  - Workspace persistence
  - Workspace sharing/collaboration
- [ ] Document operations
  - Open and view documents
  - Annotation system
  - Save document summaries
  - Tag and categorize
- [ ] Association tracking
  - Link documents to workspaces
  - Track document relationships
  - Visualize connection graphs
- [ ] Search and filter
  - Full-text search
  - Metadata filtering
  - Timeline-based queries
- [ ] Analytics and visualization
  - Generate word clouds from corpus
  - Display keyword trend line graphs over time
  - Export trend data and visualizations

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

**None currently** - Awaiting architectural decisions in Phase 0

## Questions to Resolve

1. **Communication Protocol:** WebSockets vs REST+async?
   - Consider: Real-time requirements, complexity, scalability

2. **Agent Framework:** Custom vs existing FastAgent patterns?
   - Consider: Learning curve, flexibility, maintenance

3. **3D Asset Strategy:** In-house modeling vs asset marketplace?
   - Consider: Quality, customization, timeline, cost

4. **VR/XR Priority:** Desktop-first or VR-first?
   - Consider: User accessibility, development complexity

5. **Database:** SQL vs NoSQL vs hybrid?
   - Consider: Query patterns, document structure, scalability

6. **Authentication:** Custom vs OAuth vs SSO?
   - Consider: User base, security requirements, integration

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
