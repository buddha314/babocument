# Plotly.js Integration with BabylonJS

**Created:** 2025-11-06
**Purpose:** Guide for integrating Plotly.js scientific visualizations into BabylonJS 3D scenes

## Overview

Babocument uses Plotly.js for advanced scientific visualizations (line graphs, 3D scatter plots, surface plots, heatmaps) that need to be rendered within the BabylonJS immersive environment. This guide covers three integration strategies and recommendations for different use cases.

## Why Plotly.js?

**Advantages:**
- Industry-standard scientific plotting library
- Native 3D plot support (scatter, surface, mesh)
- Rich interactivity (hover, zoom, pan, rotate)
- Extensive chart types (100+ variations)
- WebGL-accelerated rendering
- Export capabilities (PNG, SVG, JSON)
- Responsive and mobile-friendly
- Open source with active community

**Use Cases in Babocument:**
- Keyword trend line graphs (2D/3D)
- Document clustering visualizations (3D scatter)
- Research landscape topography (3D surface)
- Correlation heatmaps
- Temporal analysis charts

## Integration Strategies

### Strategy A: Canvas Texture Mapping

**Best for:** Static or infrequently updated visualizations in VR mode

**How it works:**
1. Render Plotly chart to offscreen HTML element
2. Extract canvas from Plotly's WebGL/Canvas renderer
3. Create BabylonJS texture from canvas
4. Apply texture to mesh (plane, curved panel, etc.)
5. Update texture when data changes

**Pros:**
- Full integration into 3D scene
- Works in VR/XR environments
- Can apply to curved surfaces
- No z-fighting with 3D objects
- Single WebGL context

**Cons:**
- Limited interactivity (static texture)
- Performance cost for frequent updates
- Loses Plotly's built-in hover/zoom features
- Requires manual raycasting for clicks

**Implementation:**

```typescript
import Plotly from 'plotly.js-dist';
import * as BABYLON from '@babylonjs/core';

class PlotlyTexture {
  private plotDiv: HTMLDivElement;
  private texture: BABYLON.DynamicTexture;
  private plane: BABYLON.Mesh;

  constructor(scene: BABYLON.Scene) {
    // Create offscreen div
    this.plotDiv = document.createElement('div');
    this.plotDiv.style.width = '1024px';
    this.plotDiv.style.height = '768px';
    this.plotDiv.style.position = 'absolute';
    this.plotDiv.style.left = '-9999px';
    document.body.appendChild(this.plotDiv);

    // Create dynamic texture
    this.texture = new BABYLON.DynamicTexture(
      'plotlyTexture',
      { width: 1024, height: 768 },
      scene
    );

    // Create plane mesh
    this.plane = BABYLON.MeshBuilder.CreatePlane(
      'plotPanel',
      { width: 10, height: 7.5 },
      scene
    );

    const material = new BABYLON.StandardMaterial('plotMat', scene);
    material.diffuseTexture = this.texture;
    material.emissiveColor = new BABYLON.Color3(1, 1, 1);
    this.plane.material = material;
  }

  async updatePlot(data: any[], layout: any) {
    // Render Plotly chart
    await Plotly.newPlot(this.plotDiv, data, layout, {
      staticPlot: true, // Disable interactivity for texture mode
      displayModeBar: false
    });

    // Get canvas from Plotly
    const canvas = this.plotDiv.querySelector('canvas');
    if (!canvas) return;

    // Update BabylonJS texture
    const ctx = this.texture.getContext();
    ctx.drawImage(canvas, 0, 0, 1024, 768);
    this.texture.update();
  }

  dispose() {
    document.body.removeChild(this.plotDiv);
    this.texture.dispose();
    this.plane.dispose();
  }
}

// Usage
const plotTexture = new PlotlyTexture(scene);
plotTexture.updatePlot([{
  x: [1, 2, 3, 4, 5],
  y: [10, 15, 13, 17, 20],
  type: 'scatter'
}], {
  title: 'Keyword Trends',
  xaxis: { title: 'Year' },
  yaxis: { title: 'Frequency' }
});
```

### Strategy B: HTML Overlay with Positioning

**Best for:** Desktop mode with full interactivity

**How it works:**
1. Create HTML div overlaying BabylonJS canvas
2. Render Plotly chart in overlay
3. Position and size relative to 3D scene
4. Handle pointer events separately

**Pros:**
- Full Plotly interactivity preserved
- Easy to implement
- Hover tooltips work natively
- Export features available
- Better performance for frequent updates

**Cons:**
- Not suitable for VR/XR
- Z-layering issues in complex UIs
- Doesn't integrate with 3D scene lighting
- Separate event handling needed

**Implementation:**

```typescript
import Plotly from 'plotly.js-dist';
import * as BABYLON from '@babylonjs/core';

class PlotlyOverlay {
  private overlayDiv: HTMLDivElement;
  private scene: BABYLON.Scene;

  constructor(scene: BABYLON.Scene, containerId: string) {
    this.scene = scene;

    // Create overlay container
    this.overlayDiv = document.createElement('div');
    this.overlayDiv.id = containerId;
    this.overlayDiv.style.position = 'absolute';
    this.overlayDiv.style.top = '50px';
    this.overlayDiv.style.right = '50px';
    this.overlayDiv.style.width = '600px';
    this.overlayDiv.style.height = '400px';
    this.overlayDiv.style.backgroundColor = 'rgba(255, 255, 255, 0.95)';
    this.overlayDiv.style.borderRadius = '8px';
    this.overlayDiv.style.padding = '10px';
    this.overlayDiv.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
    this.overlayDiv.style.pointerEvents = 'auto';
    this.overlayDiv.style.zIndex = '100';

    document.body.appendChild(this.overlayDiv);
  }

  async renderPlot(data: any[], layout: any) {
    const config = {
      responsive: true,
      displayModeBar: true,
      displaylogo: false,
      modeBarButtonsToRemove: ['lasso2d', 'select2d']
    };

    await Plotly.newPlot(this.overlayDiv, data, layout, config);
  }

  setPosition(x: number, y: number) {
    this.overlayDiv.style.left = `${x}px`;
    this.overlayDiv.style.top = `${y}px`;
  }

  show() {
    this.overlayDiv.style.display = 'block';
  }

  hide() {
    this.overlayDiv.style.display = 'none';
  }

  dispose() {
    Plotly.purge(this.overlayDiv);
    document.body.removeChild(this.overlayDiv);
  }
}

// Usage
const overlay = new PlotlyOverlay(scene, 'trend-graph');
overlay.renderPlot([{
  x: [2015, 2016, 2017, 2018, 2019, 2020],
  y: [23, 45, 67, 89, 102, 134],
  type: 'scatter',
  mode: 'lines+markers',
  name: 'Bioink'
}], {
  title: 'Keyword Frequency Over Time',
  xaxis: { title: 'Year' },
  yaxis: { title: 'Mentions' }
});
```

### Strategy C: Native BabylonJS Conversion

**Best for:** Maximum VR performance and custom styling

**How it works:**
1. Extract data from Plotly-compatible format
2. Create native BabylonJS meshes (lines, points, surfaces)
3. Implement custom interactions with BabylonJS
4. Full control over rendering and optimization

**Pros:**
- Best VR/XR performance
- Full integration with scene lighting/shaders
- Custom interactions with 3D controllers
- No external dependencies after data extraction
- Single WebGL context

**Cons:**
- Most development effort
- Must reimplement chart features
- Loses Plotly's rich ecosystem
- Maintenance burden for updates

**Implementation:**

```typescript
import * as BABYLON from '@babylonjs/core';

class Native3DPlot {
  private scene: BABYLON.Scene;
  private meshes: BABYLON.Mesh[] = [];

  constructor(scene: BABYLON.Scene) {
    this.scene = scene;
  }

  createLineGraph(data: { x: number[], y: number[], z?: number[] }, options: any) {
    const points: BABYLON.Vector3[] = [];

    // Convert data to 3D points
    for (let i = 0; i < data.x.length; i++) {
      points.push(new BABYLON.Vector3(
        data.x[i],
        data.y[i],
        data.z ? data.z[i] : 0
      ));
    }

    // Create line mesh
    const lines = BABYLON.MeshBuilder.CreateLines('graph-line', {
      points: points
    }, this.scene);

    lines.color = BABYLON.Color3.FromHexString(options.color || '#1f77b4');
    this.meshes.push(lines);

    // Create data point markers
    points.forEach((point, index) => {
      const sphere = BABYLON.MeshBuilder.CreateSphere(
        `point-${index}`,
        { diameter: 0.2 },
        this.scene
      );
      sphere.position = point;

      const material = new BABYLON.StandardMaterial('pointMat', this.scene);
      material.diffuseColor = BABYLON.Color3.FromHexString(options.color || '#1f77b4');
      material.emissiveColor = material.diffuseColor;
      sphere.material = material;

      this.meshes.push(sphere);

      // Add interaction
      sphere.actionManager = new BABYLON.ActionManager(this.scene);
      sphere.actionManager.registerAction(
        new BABYLON.ExecuteCodeAction(
          BABYLON.ActionManager.OnPickTrigger,
          () => {
            console.log('Clicked point:', index, data.x[index], data.y[index]);
            // Show tooltip, highlight, etc.
          }
        )
      );
    });

    return lines;
  }

  create3DScatter(data: { x: number[], y: number[], z: number[], size?: number[] }) {
    const sps = new BABYLON.SolidParticleSystem('scatter', this.scene);

    // Create particles for each data point
    sps.addShape(
      BABYLON.MeshBuilder.CreateSphere('', { diameter: 1 }, this.scene),
      data.x.length
    );

    const mesh = sps.buildMesh();

    sps.initParticles = () => {
      for (let i = 0; i < sps.nbParticles; i++) {
        const particle = sps.particles[i];
        particle.position = new BABYLON.Vector3(data.x[i], data.y[i], data.z[i]);
        particle.scaling = new BABYLON.Vector3(
          data.size ? data.size[i] : 1,
          data.size ? data.size[i] : 1,
          data.size ? data.size[i] : 1
        );
      }
    };

    sps.initParticles();
    sps.setParticles();

    this.meshes.push(mesh);
    return mesh;
  }

  dispose() {
    this.meshes.forEach(mesh => mesh.dispose());
    this.meshes = [];
  }
}

// Usage
const nativePlot = new Native3DPlot(scene);
nativePlot.createLineGraph({
  x: [2015, 2016, 2017, 2018, 2019, 2020],
  y: [23, 45, 67, 89, 102, 134]
}, {
  color: '#ff6b6b'
});
```

## Recommended Approach: Hybrid Strategy

**Use different strategies based on context:**

```typescript
class HybridVisualizationManager {
  private scene: BABYLON.Scene;
  private mode: 'desktop' | 'vr';

  constructor(scene: BABYLON.Scene) {
    this.scene = scene;
    this.mode = this.detectMode();
  }

  detectMode(): 'desktop' | 'vr' {
    // Check if VR device is active
    return this.scene.activeCamera?.getClassName().includes('VR') ? 'vr' : 'desktop';
  }

  async showTrendGraph(data: any[], layout: any) {
    if (this.mode === 'desktop') {
      // Use Strategy B: HTML Overlay for full interactivity
      const overlay = new PlotlyOverlay(this.scene, 'trend-graph');
      await overlay.renderPlot(data, layout);
    } else {
      // Use Strategy A: Texture mapping for VR
      const texture = new PlotlyTexture(this.scene);
      await texture.updatePlot(data, layout);
    }
  }

  async show3DScatter(data: any[]) {
    // Always use Strategy C for 3D scatter in VR (best performance)
    const nativePlot = new Native3DPlot(this.scene);
    nativePlot.create3DScatter({
      x: data[0].x,
      y: data[0].y,
      z: data[0].z
    });
  }
}
```

## WebGL Context Management

**Challenge:** Both Plotly 3D and BabylonJS use WebGL contexts. Browsers limit total contexts.

**Solutions:**

### 1. Share Canvas Context (Advanced)
```typescript
// Use same canvas for both (requires custom Plotly build)
const sharedCanvas = document.getElementById('renderCanvas');
// Not easily achievable with standard Plotly
```

### 2. Context Reuse
```typescript
// Dispose Plotly contexts when not in use
Plotly.purge(plotDiv); // Releases WebGL context

// Recreate when needed
Plotly.newPlot(plotDiv, data, layout);
```

### 3. Fallback to 2D
```typescript
// Check WebGL context availability
const maxContexts = 16; // Browser dependent
if (activeContextCount >= maxContexts) {
  // Fall back to 2D charts
  layout.type = 'scatter'; // instead of scatter3d
}
```

### 4. Use Plotly Basic Bundle
```typescript
// Import smaller bundle without 3D support if not needed
import Plotly from 'plotly.js-basic-dist';
// Saves ~1MB and reduces WebGL pressure
```

## Performance Optimization

### 1. Lazy Loading
```typescript
// Only load Plotly when visualization needed
const loadPlotly = async () => {
  if (!window.Plotly) {
    window.Plotly = await import('plotly.js-dist');
  }
  return window.Plotly;
};
```

### 2. Downsampling Large Datasets
```typescript
function downsample(data: number[], targetSize: number) {
  const step = Math.ceil(data.length / targetSize);
  return data.filter((_, i) => i % step === 0);
}

// Use for trends with thousands of points
const downsampledData = downsample(originalData, 500);
```

### 3. Update Instead of Recreate
```typescript
// More efficient than Plotly.newPlot
Plotly.update(plotDiv, dataUpdate, layoutUpdate);
```

### 4. Static Plot Mode for Textures
```typescript
// Disable animations and interactions for texture rendering
const config = {
  staticPlot: true,
  displayModeBar: false
};
```

## Installation

### NPM Package
```bash
npm install plotly.js-dist
# or for smaller bundle
npm install plotly.js-basic-dist
```

### TypeScript Definitions
```bash
npm install --save-dev @types/plotly.js
```

### package.json
```json
{
  "dependencies": {
    "plotly.js-dist": "^2.28.0",
    "@babylonjs/core": "^8.33.2"
  },
  "devDependencies": {
    "@types/plotly.js": "^2.12.29"
  }
}
```

## Testing Strategy

### Unit Tests
- Test data transformation functions
- Verify texture creation from canvas
- Check memory cleanup (dispose methods)

### Integration Tests
- BabylonJS + Plotly rendering together
- Context management under load
- Mode switching (desktop ↔ VR)

### Performance Tests
- FPS with multiple plots active
- Memory usage over time
- WebGL context limit handling

## Examples

### Keyword Trend Visualization
```typescript
const trendData = [{
  x: [2015, 2016, 2017, 2018, 2019, 2020, 2021],
  y: [23, 45, 67, 89, 102, 134, 156],
  type: 'scatter',
  mode: 'lines+markers',
  name: 'Bioink',
  line: { color: '#1f77b4', width: 3 }
}, {
  x: [2015, 2016, 2017, 2018, 2019, 2020, 2021],
  y: [12, 18, 25, 42, 67, 89, 98],
  type: 'scatter',
  mode: 'lines+markers',
  name: 'CRISPR',
  line: { color: '#ff7f0e', width: 3 }
}];

const layout = {
  title: 'Research Keyword Trends',
  xaxis: { title: 'Publication Year' },
  yaxis: { title: 'Frequency' },
  hovermode: 'closest'
};
```

### 3D Document Clustering
```typescript
const clusterData = [{
  x: [1, 2, 3, 4, 5],
  y: [2, 4, 1, 5, 3],
  z: [3, 1, 4, 2, 5],
  mode: 'markers',
  type: 'scatter3d',
  marker: {
    size: 12,
    color: ['red', 'blue', 'green', 'red', 'blue'],
    opacity: 0.8
  }
}];

const layout3d = {
  title: 'Document Similarity Space',
  scene: {
    xaxis: { title: 'Topic Relevance' },
    yaxis: { title: 'Citation Count' },
    zaxis: { title: 'Recency' }
  }
};
```

## Troubleshooting

### Issue: Texture appears black
**Solution:** Ensure canvas is fully rendered before creating texture
```typescript
await Plotly.newPlot(plotDiv, data, layout);
await new Promise(resolve => setTimeout(resolve, 100)); // Wait for render
const canvas = plotDiv.querySelector('canvas');
```

### Issue: WebGL context lost
**Solution:** Implement context loss handlers
```typescript
canvas.addEventListener('webglcontextlost', (e) => {
  e.preventDefault();
  // Dispose and recreate
});
```

### Issue: Poor VR performance
**Solution:** Use native BabylonJS meshes (Strategy C) or reduce plot complexity

## References

- [Plotly.js Documentation](https://plotly.com/javascript/)
- [BabylonJS Textures](https://doc.babylonjs.com/features/featuresDeepDive/materials/using/materials_introduction)
- [WebGL Context Management](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API)
- [VISUALIZATION_REQUIREMENTS.md](../specs/VISUALIZATION_REQUIREMENTS.md)

## Related Documentation

- [TASKS.md](../specs/TASKS.md) - Phase 3 visualization tasks
- [VISUALIZATION_REQUIREMENTS.md](../specs/VISUALIZATION_REQUIREMENTS.md) - Complete requirements
- [README.md](../README.md) - Project overview
