# Visualization Requirements - Babocument

**Created:** 2025-11-06
**Owner:** Beabadoo (Primary User Persona)

## Overview

Babocument provides rich data visualizations to help Beabadoo understand trends, patterns, and the evolution of research topics over time. Visualizations are integrated into the immersive VR/XR environment and accessible through traditional 2D UI panels.

**Visualization Library:** Plotly.js will be used for scientific plotting capabilities, with special integration strategies for rendering within BabylonJS 3D scenes.

## Core Visualization Types

### 1. Keyword Trend Line Graphs

**Purpose:** Display temporal trends of keyword frequency across the research corpus

**User Story:**
> As Beabadoo, I want to see how frequently specific keywords appear in research papers over time, so I can understand the evolution and popularity of research topics in biomanufacturing.

**Requirements:**

#### Data Source
- Analyze full-text articles from the user's corpus
- Extract keyword frequencies by publication year
- Support custom keyword selection
- Track multiple keywords simultaneously

#### Visualization Features
- **X-axis:** Time (publication years)
- **Y-axis:** Keyword frequency/occurrence count
- **Multi-line support:** Compare up to 10 keywords on same graph
- **Interactive legend:** Toggle individual keyword lines on/off
- **Data points:** Show exact values on hover
- **Time range selection:** Filter to specific year ranges
- **Normalization options:**
  - Absolute count (raw number of mentions)
  - Relative frequency (per 1000 documents)
  - Percentage of total corpus

#### Interactions
- Hover over data points to see exact values
- Click data point to view source documents from that year
- Zoom into specific time ranges
- Pan across timeline
- Export graph as PNG/SVG
- Export underlying data as CSV/JSON

#### Visual Design
- Clean, scientific aesthetic matching project style
- Color-coded lines (distinct, accessible colors)
- Grid lines for readability
- Smooth line rendering (cubic interpolation)
- Responsive to window/panel resizing

#### Technical Implementation
- **Frontend:** Plotly.js for 2D/3D line graphs
- **3D Rendering Options:**
  - **Option A:** Render Plotly to offscreen canvas, texture-map to BabylonJS plane mesh
  - **Option B:** Use Plotly 3D mode (plotly.js 3D scatter/surface) in overlay
  - **Option C:** Convert Plotly data to native BabylonJS meshes for full VR integration
- **Backend:** Analysis Agent calculates trend data
- **API Endpoint:** `/api/analytics/keyword-trends`
- **Caching:** Pre-computed trends for common keywords

### 2. Word Clouds

**Purpose:** Visual representation of keyword importance and frequency

**User Story:**
> As Beabadoo, I want to see which keywords dominate my research corpus, so I can quickly understand the main themes and topics.

**Requirements:**

#### Data Source
- TF-IDF analysis across corpus
- Exclude common scientific stop words
- Configurable time range filtering
- Workspace-specific or global corpus analysis

#### Visualization Features
- Font size represents frequency/importance
- Color represents category or recency
- Interactive word selection
- Animated transitions when filtering
- Maximum 100 words displayed

#### Interactions
- Click word to generate trend line graph
- Hover to show exact frequency
- Filter by year range
- Filter by document workspace
- Export as image

### 3. Agent-Assisted Paper Discovery

**Purpose:** Enable natural language queries to find relevant scientific papers using AI agents

**User Story:**
> As Beabadoo, I want to ask the agent to find scientific papers for me using natural language, so I can quickly discover relevant research without manually searching through databases.

**Requirements:**

#### Query Interface
- Natural language query input (e.g., "Find papers about bioink formulation published after 2020")
- Voice input support for hands-free operation in VR
- Query history and favorites
- Suggested queries based on workspace context

#### Agent Capabilities
- **Research Agent** processes natural language queries
- Semantic search across local corpus and external repositories
- Relevance ranking using embedding similarity
- Filter by year, author, journal, document type
- Cross-reference with ClinicalTrials.gov for biomedical papers

#### Query Types Supported
- Keyword-based: "papers about CRISPR"
- Author-based: "papers by Jennifer Doudna"
- Topic-based: "recent advances in synthetic biology"
- Comparative: "compare bioink materials for tissue engineering"
- Time-ranged: "papers from last 5 years about biomanufacturing"
- Citation-based: "papers citing [specific paper]"

#### Response Format
- Ranked list of relevant papers
- Relevance score (0-1) displayed
- Brief AI-generated summary for each result
- Highlighting of query-relevant sections
- "Why this matches" explanation from agent
- Option to view full document or add to workspace

#### Interactions
- Click result to view full paper
- Add to current workspace
- Generate comparative summary of top results
- Ask follow-up questions to refine search
- Save search query for later reuse
- Export results as bibliography (BibTeX, RIS)

#### Visual Presentation
- Results displayed in panel overlay
- 3D timeline integration (highlight matching documents)
- Agent avatar shows "thinking" animation during search
- Progress indicator for multi-source searches
- Result cards with metadata and thumbnails

#### Technical Implementation
- **Frontend:** SearchBar component with natural language support
- **Backend:** Research Agent with LLM integration
- **API Endpoints:**
  - `POST /api/v1/agents/search` - Natural language query
  - `GET /api/v1/agents/search/{task_id}` - Search progress
  - `POST /api/v1/agents/search/{task_id}/refine` - Refine results
- **Real-time Updates:** WebSocket events for search progress
- **Caching:** Cache common queries and results

#### Performance Requirements
- Initial results within 2 seconds (local corpus)
- External repository results within 5 seconds
- Support concurrent searches
- Queue management for multiple users

#### Example Queries
```
"Find papers about bioink formulation for 3D printing"
"Show me recent advances in CRISPR gene editing"
"Papers by George Church about synthetic biology"
"Compare different methods for tissue scaffolding"
"What's new in biomanufacturing since 2023?"
"Papers about CAR-T cell therapy with clinical trial data"
```

### 4. Timeline Visualization

**Purpose:** Spatial representation of document distribution over time

**User Story:**
> As Beabadoo, I want to navigate through research chronologically in an immersive environment, so I can understand how knowledge has evolved.

**Requirements:**

#### Visual Representation
- 3D corridor descending through time
- Glass partitions separating years
- Document cards positioned by date
- Year labels prominently displayed
- Density visualization (more documents = denser space)

#### Interactions
- Walk/fly through timeline
- Jump to specific years
- Filter documents by keyword (highlights in space)
- Scrubbing timeline control (2D UI)

### 4. Journal Repository Management

**Purpose:** Allow Beabadoo to discover, list, edit, and organize journal repositories

**User Story:**
> As Beabadoo, I want to manage a list of journal repositories so I can discover new sources and organize them into workspaces for different research projects.

**Requirements:**

#### Repository Discovery
- Search for and discover new journal repositories
- Preview repository metadata (name, description, coverage)
- Test repository connectivity and availability
- View sample articles from repository

#### Repository List Management
- View all configured journal repositories
- Add new repository connections
  - arXiv (preprints)
  - PubMed/PubMed Central
  - bioRxiv/medRxiv
  - Custom institutional repositories
  - Custom API endpoints
- Edit repository configuration
  - Update API keys/credentials
  - Modify search parameters
  - Set priority/relevance for searches
- Remove repositories from active list
- Enable/disable repositories without deletion
- Categorize repositories by research domain

#### Workspace Integration
- Assign repositories to specific workspaces
- Workspace-scoped search (only selected repositories)
- Global search (all active repositories)
- Track which repositories contributed to each workspace
- Repository usage statistics per workspace

#### Data Management
- **Storage:** Configuration stored in database
- **API Endpoint:** `/api/repositories`
  - `GET /api/repositories` - List all repositories
  - `POST /api/repositories` - Add new repository
  - `PUT /api/repositories/{id}` - Update repository
  - `DELETE /api/repositories/{id}` - Remove repository
  - `POST /api/repositories/{id}/test` - Test connection
- **Permissions:** User-scoped repository lists
- **Validation:** Test connectivity before saving

#### UI Components
- Repository management panel
- Repository card with status indicators
- Quick add from repository marketplace
- Drag-and-drop to assign to workspaces
- Connection status indicators (online/offline/rate-limited)

### 5. Document Relationship Graphs

**Purpose:** Visualize connections between research papers

**Requirements:**
- Node-link diagram showing document citations
- Cluster similar topics
- Show influence paths
- Interactive exploration

### 6. 3D Scientific Plots (Plotly.js)

**Purpose:** Advanced scientific visualizations in immersive 3D space

**User Story:**
> As Beabadoo, I want to see multi-dimensional data relationships in 3D space, so I can discover patterns and correlations that are difficult to visualize in 2D.

**Supported Plot Types:**

#### 3D Scatter Plots
- Visualize document clustering in topic space
- X/Y/Z axes represent different dimensions (time, citations, relevance)
- Color represents categories or metrics
- Size represents importance or frequency
- Interactive rotation and zoom

#### 3D Surface Plots
- Keyword frequency heatmaps over time and categories
- Research landscape topography
- Smooth interpolation between data points
- Color gradients for value ranges

#### 3D Line Plots
- Trajectory of research trends through multi-dimensional space
- Multiple keyword evolution paths
- Temporal progression visualization

#### Heatmaps & Contour Plots
- Correlation matrices
- Co-occurrence patterns
- Publication density over time × topic

**Technical Implementation with Plotly.js:**

**Integration Strategy A: Canvas Texture Mapping**
```typescript
// Render Plotly to offscreen canvas
const plotDiv = document.createElement('div');
Plotly.newPlot(plotDiv, data, layout, config);

// Convert to texture
const canvas = plotDiv.querySelector('canvas');
const texture = new BABYLON.Texture.CreateFromCanvas(canvas);

// Apply to mesh in BabylonJS
const plane = BABYLON.MeshBuilder.CreatePlane("plot", {size: 10});
plane.material.diffuseTexture = texture;
```

**Integration Strategy B: HTML Overlay with WebGL**
```typescript
// Plotly in overlay div with transparent background
const overlay = document.getElementById('plotly-overlay');
Plotly.newPlot(overlay, data, layout, {
  displayModeBar: true,
  responsive: true
});

// Positioned over BabylonJS canvas
overlay.style.position = 'absolute';
overlay.style.pointerEvents = 'auto';
```

**Integration Strategy C: Native BabylonJS Conversion**
```typescript
// Convert Plotly data to BabylonJS meshes
function plotlyToBabylon(plotlyData) {
  const points = plotlyData[0].x.map((x, i) =>
    new BABYLON.Vector3(x, plotlyData[0].y[i], plotlyData[0].z[i])
  );

  // Create point cloud or mesh
  const sps = new BABYLON.SolidParticleSystem("points", scene);
  // ... render particles for each data point
}
```

**Recommended Approach:**
- **Desktop Mode:** Strategy B (HTML overlay) for full Plotly interactivity
- **VR Mode:** Strategy A or C (texture/native) for performance and immersion
- **Hybrid:** Detect mode and switch strategies automatically

## UI Integration

### 3D Environment Integration

**In-World Panels:**
- Floating 2D panels in VR space
- Anchored to workspace areas
- Scalable and repositionable
- Always face user (billboard mode)

**Locations:**
- Virtual lab workstations
- Librarian's desk area
- Floating panels in File Room

### 2D UI Overlay

**Desktop Mode:**
- Sidebar panels
- Modal overlays for detailed views
- Dashboard landing page
- Export controls

**VR/XR Mode:**
- Hand-held tablet metaphor
- Gesture-controlled panels
- Voice-activated visualization requests

## Data Processing Pipeline

### Backend Architecture

```
User Query → Research Agent → Analysis Agent → Visualization Data

Analysis Agent:
1. Query corpus database
2. Extract keyword frequencies
3. Aggregate by time period
4. Calculate trends and statistics
5. Cache results
6. Return JSON payload
```

### API Endpoints

**Keyword Trends:**
```
GET /api/analytics/keyword-trends
Query Parameters:
  - keywords: string[] (comma-separated)
  - startYear: number
  - endYear: number
  - workspace: string (optional)
  - normalization: "absolute" | "relative" | "percentage"

Response:
{
  "trends": [
    {
      "keyword": "bioink",
      "data": [
        {"year": 2020, "count": 45, "documents": 120},
        {"year": 2021, "count": 67, "documents": 150}
      ]
    }
  ],
  "metadata": {
    "totalDocuments": 1500,
    "yearRange": [2015, 2025]
  }
}
```

**Word Cloud Data:**
```
GET /api/analytics/word-cloud
Query Parameters:
  - workspace: string (optional)
  - startYear: number
  - endYear: number
  - maxWords: number (default: 100)

Response:
{
  "words": [
    {"text": "bioink", "weight": 0.95, "count": 450},
    {"text": "bioprinting", "weight": 0.82, "count": 380}
  ]
}
```

## Performance Requirements

### Response Time
- Keyword trend query: < 500ms for cached data
- Word cloud generation: < 1s for 1000 documents
- Graph rendering: 60 FPS smooth animations

### Scalability
- Support corpus up to 100,000 documents
- Handle 10 concurrent keyword trend queries
- Real-time updates when new documents added

### Caching Strategy
- Pre-compute trends for top 100 keywords
- Cache workspace-specific visualizations
- Invalidate cache on corpus updates
- Redis or in-memory cache

## Accessibility

- High contrast mode for visualizations
- Screen reader compatible (2D UI)
- Keyboard navigation for all interactions
- Adjustable font sizes
- Color-blind friendly palettes

## Future Enhancements

### Phase 1 (Current Requirements)
- ✓ Keyword trend line graphs
- ✓ Word clouds
- ✓ Basic timeline visualization

### Phase 2 (Future)
- Citation network graphs
- Co-occurrence matrices
- Geographic distribution maps
- Sentiment analysis over time
- Author collaboration networks

### Phase 3 (Advanced)
- Real-time collaboration (multi-user viewing)
- AI-powered insight annotations
- Predictive trend forecasting
- Comparative corpus analysis
- 3D data landscapes in VR

## Success Metrics

**Adoption:**
- 80% of users generate at least one trend graph per session
- Average 5 keyword trend queries per research session

**Performance:**
- 95% of queries return in < 1s
- Zero visualization rendering errors

**User Satisfaction:**
- Beabadoo finds trend graphs "very useful" (5/5 rating)
- Reduces time to identify research trends by 50%

## Technical Dependencies

**Required:**
- **Plotly.js** (v2.x) - Primary visualization library
  - plotly.js-dist (full bundle) or plotly.js-basic-dist (smaller)
  - WebGL support for 3D plots
  - NPM: `npm install plotly.js-dist`
- Analysis Agent (Phase 5)
- Corpus database with full-text indexing
- Time-series data storage
- BabylonJS GUI for panel integration

**Optional:**
- GPU acceleration for large datasets
- Offscreen canvas API for texture rendering
- Export service for high-res images
- D3.js (if needed for custom visualizations beyond Plotly)

**WebGL Context Considerations:**
- Plotly 3D plots use WebGL (same as BabylonJS)
- May need to manage shared WebGL context or use separate contexts
- Test for WebGL context limit on target browsers
- Consider fallback to 2D plots on low-end hardware

## Testing Requirements

### Unit Tests
- Keyword frequency calculation accuracy
- Trend aggregation logic
- Normalization algorithms
- Data export formats

### Integration Tests
- End-to-end API to UI rendering
- Multi-keyword trend queries
- Workspace filtering
- Cache invalidation

### User Testing
- Beabadoo persona validation
- Usability testing with scientists
- VR interaction testing
- Performance testing with large corpus

## Documentation

**For Developers:**
- API endpoint documentation
- Visualization component library
- Data format specifications
- Performance optimization guide

**For Users:**
- Tutorial: Creating keyword trend graphs
- Guide: Interpreting visualizations
- FAQ: Common analysis questions
- Video: Navigating temporal data

## Related Documents

- [TASKS.md](TASKS.md) - Phase 5 (Analysis Agent), Phase 6 (Visualization UI)
- [PROJECT_STATUS.md](PROJECT_STATUS.md) - Feature status tracking
- [README.md](../README.md) - Feature overview
- [BEABADOO_PERSONA.md](BEABADOO_PERSONA.md) - User needs (if created)
