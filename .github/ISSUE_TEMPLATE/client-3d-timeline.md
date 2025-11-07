---
name: 3D Timeline Visualization (Client)
about: Integrate API data with BabylonJS 3D timeline corridor
title: '3D Timeline Visualization (Client)'
labels: 'client, babylonjs, 3d, visualization, P2, phase-3'
assignees: ''
---

## Summary

Create an immersive 3D timeline corridor in BabylonJS that visualizes documents from the API sorted by year, with interactive selection and search result highlighting.

## Background

This is the core visualization feature of Babocument - a virtual "file room" where users descend through time to explore research documents. Documents are represented as 3D objects positioned along a timeline, organized by year.

**User Experience:**
- Descend through corridor (moving backward in time)
- Glass partitions separate years
- Document cards float in 3D space
- Click/select to view document details
- Search results highlighted with glow effect
- VR controller support for selection

## Tasks

### 1. Create Timeline3D Component
- [ ] Create `client/src/components/babylon/Timeline3D.tsx`
  - Set up BabylonJS scene
  - Create camera (first-person or free camera)
  - Add lighting (ambient + directional)
  - Create timeline corridor structure
  - Add glass year partitions

### 2. Generate Document Meshes from API Data
- [ ] Create `client/src/components/babylon/DocumentMesh.tsx`
  - Create mesh for each document
  - Display title as 3D text or texture
  - Show metadata (authors, year, source)
  - Add hover effect
  - Add click handling
  - Optimize for large document counts

### 3. Position Documents by Year
- [ ] Sort documents by year
- [ ] Calculate positions along Z-axis (timeline)
- [ ] Group documents within same year
- [ ] Add year labels (floating text)
- [ ] Create glass partitions between years
- [ ] Add distance markers

### 4. Add Interactive Selection
- [ ] Implement ray casting for selection
- [ ] Highlight on hover (outline/glow)
  - Select on click
  - Show document details in UI panel
  - Smooth camera transition to selected document

### 5. Integrate Search Results
- [ ] Receive search results from SearchBar
  - Highlight matching documents (different color/glow)
  - Dim non-matching documents
  - Camera animation to first result
  - Add "Next Result" navigation

### 6. VR/XR Support
- [ ] Add VR controller support
  - Pointer ray for selection
  - Teleportation between years
  - Grab and examine documents
  - UI overlay in VR space

### 7. Performance Optimization
- [ ] Level of Detail (LOD) for distant documents
- [ ] Frustum culling
- [ ] Mesh instancing for similar objects
- [ ] Lazy loading (load documents as user approaches)
- [ ] Target 60+ FPS in VR

## Files to Create

```
client/src/components/babylon/
├── Timeline3D.tsx           # Main timeline scene
├── DocumentMesh.tsx         # Individual document representation
├── YearPartition.tsx        # Glass year dividers
├── TimelineNavigation.tsx   # Navigation controls
└── utils/
    ├── meshGeneration.ts    # Helper functions for mesh creation
    └── positioning.ts       # Document positioning logic
```

## Acceptance Criteria

- [ ] Documents load from API and render in 3D
- [ ] Documents sorted by year along timeline
- [ ] Can navigate through timeline (keyboard/VR controllers)
- [ ] Can select documents (click/ray cast)
- [ ] Selected document shows details in UI
- [ ] Search results are highlighted
- [ ] Year partitions visible between years
- [ ] Smooth camera animations
- [ ] Works in desktop mode
- [ ] Works in VR/XR mode
- [ ] Maintains 60+ FPS with 100+ documents
- [ ] Handles empty states gracefully

## Code Example

**Timeline3D Component:**
```typescript
'use client';

import { useEffect, useRef } from 'react';
import { Scene, Engine, UniversalCamera, Vector3 } from '@babylonjs/core';
import { useDocuments } from '@/lib/hooks/useDocuments';

export function Timeline3D() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const { data: documents } = useDocuments({ limit: 100 });

  useEffect(() => {
    if (!canvasRef.current || !documents) return;

    const engine = new Engine(canvasRef.current);
    const scene = new Scene(engine);

    // Camera
    const camera = new UniversalCamera('camera', new Vector3(0, 1.6, 0), scene);
    camera.attachControl();

    // Create document meshes
    documents.documents.forEach((doc, index) => {
      const position = calculatePosition(doc.year, index);
      createDocumentMesh(doc, position, scene);
    });

    engine.runRenderLoop(() => scene.render());

    return () => {
      scene.dispose();
      engine.dispose();
    };
  }, [documents]);

  return <canvas ref={canvasRef} className="w-full h-full" />;
}

function calculatePosition(year: number, index: number): Vector3 {
  const baseYear = 2000;
  const z = (year - baseYear) * 10; // 10 units per year
  const x = (index % 5) * 2 - 4; // Arrange in columns
  const y = 1.5; // Eye level
  return new Vector3(x, y, z);
}
```

## Dependencies

- **Depends on:** Issue #32 (Document API Integration)
- **Related to:** Issue #33 (Search Integration - for highlighting)

## Estimated Time

12-16 hours

## Phase

Phase 3 - Frontend Visualization

## Related Issues

- Issue #32 - Document API Integration (dependency)
- Issue #33 - Search Integration (for result highlighting)
- Issue #7 - Blender Asset Pipeline (for 3D assets)
- Issue #11 - Data Visualization UI (epic)

## Design Considerations

**Timeline Layout:**
- Each year = 10 units along Z-axis
- Documents arranged in grid within year
- Glass partitions at year boundaries
- Year labels floating above partitions

**Visual Design:**
- Document cards: Transparent panels with text
- Hover: Glow effect + outline
- Selected: Bright highlight + scale up
- Search match: Green glow
- Non-match: Faded opacity

**Performance:**
- Use mesh instancing for cards
- LOD system for distant documents
- Lazy load content on approach
- Optimize for 1000+ documents

## Testing

- [ ] Test with 10 documents
- [ ] Test with 100 documents
- [ ] Test with 1000 documents
- [ ] Test search highlighting
- [ ] Test VR mode
- [ ] Test performance (FPS counter)
- [ ] Test empty state (no documents)
- [ ] Test single year
- [ ] Test documents without years

## Future Enhancements

- [ ] Add "Librarian" character NPC
- [ ] Add ambient sounds
- [ ] Add particle effects
- [ ] Add mini-map navigation
- [ ] Add bookmark/favorite system
- [ ] Add collaborative features (see other users)

## Documentation

- BabylonJS Docs: https://doc.babylonjs.com/
- See `CLIENT_API_INTEGRATION_PLAN.md` for data flow
- See `docs/BLENDER_WORKFLOW.md` for asset creation
