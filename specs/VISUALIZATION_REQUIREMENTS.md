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

### 3. Timeline Visualization

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

### 4. Document Relationship Graphs

**Purpose:** Visualize connections between research papers

**Requirements:**
- Node-link diagram showing document citations
- Cluster similar topics
- Show influence paths
- Interactive exploration

### 5. 3D Scientific Plots (Plotly.js)

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
