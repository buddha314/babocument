# Quick Reference: Babylon.js Client Structure

## File Locations

| Purpose | Path | Lines | Key Info |
|---------|------|-------|----------|
| Main Scene | `client/src/app/page.tsx` | 108 | Engine, Scene, Physics init |
| Scripts Registry | `client/src/scripts.ts` | 14 | Maps scripts to modules |
| Example Script | `client/src/scripts/box.ts` | 21 | Pattern for new scripts |
| Scene Config | `client/assets/example.scene/config.json` | 217 | Camera, lights, meshes |
| Dependencies | `client/package.json` | 34 | BJS 8.33.2, Next 14.2.32 |
| Types | `client/tsconfig.json` | 41 | Decorators enabled |
| Build Config | `client/next.config.js` | 14 | Shader loader for .fx files |

## Critical Code Sections

### Engine Initialization (page.tsx, lines 53-62)
```
Engine Options:
- stencil: true (REQUIRED for XR)
- antialias: true
- audioEngine: true
- useHighPrecisionFloats: true
- powerPreference: "high-performance"
```

### Physics Setup (page.tsx, lines 82-83)
```
Havok Plugin initialization
Gravity: (0, -981, 0)
```

### Scene Loading (page.tsx, line 86)
```
loadScene("/scene/", "example.babylon", scene, scriptsMap)
Note: Scene files must be in public/scene/ folder
```

### Render Loop (page.tsx, lines 94-96)
```
engine.runRenderLoop(() => scene.render())
Runs every frame
```

## Script Pattern (from box.ts)

```typescript
import { Mesh } from "@babylonjs/core/Meshes/mesh";
import { IScript, visibleAsNumber } from "babylonjs-editor-tools";

export default class MyScript implements IScript {
    @visibleAsNumber("Property Name", { min: 0, max: 1 })
    private _property: number = 0.5;

    constructor(public mesh: Mesh) {}

    onStart(): void {}
    onUpdate(): void {}
}
```

## Babylon.js Packages

- @babylonjs/core: 8.33.2 - Main engine
- @babylonjs/gui: 8.33.2 - UI widgets
- @babylonjs/havok: 1.3.10 - Physics
- @babylonjs/materials: 8.33.2 - Materials library
- babylonjs-editor-tools: latest - Scene loader

## WebXR Key Imports Needed

```typescript
import { WebXRExperienceHelper } from "@babylonjs/core/XR/webXRExperienceHelper";
import { WebXRControllerPointerSelection } from "@babylonjs/core/XR/features/WebXRControllerPointerSelection";
import { WebXRMotionControllerTeleportation } from "@babylonjs/core/XR/features/WebXRMotionControllerTeleportation";
import { WebXRState } from "@babylonjs/core/XR/webXRTypes";
```

## Initialization Order in handleLoad

1. Initialize Havok physics
2. Enable physics on scene
3. Set scene loader flags
4. Load scene from file
5. Attach camera control
6. Start render loop

**For WebXR, add after step 1 (physics) and before step 3**

## Assets

Location: `client/assets/`

- example.scene/ - BJS Editor export
  - 3 meshes with physics
  - 1 directional light with shadows
  - 1 camera
  - Materials and textures

- country.env (3.8MB) - HDR environment map

## Directory Structure (Client)

```
client/
├── src/app/page.tsx         ← MAIN FILE
├── src/scripts/*.ts         ← Add new scripts here
├── src/scripts.ts           ← Update when adding scripts
├── assets/example.scene/    ← Scene definition
├── public/                  ← Deployed assets (needs scene files)
├── package.json             ← Dependencies
└── tsconfig.json            ← Type config
```

## Key Canvas Setup

- Full screen (w-full h-full)
- useRef for canvas element
- React useEffect for lifecycle
- Client-side rendering ("use client")

## Development

```bash
cd client
npm install
npm run dev
# Visit http://localhost:3000
```

## Testing Checklist

Desktop:
- [ ] Scene renders
- [ ] Physics works (gravity)
- [ ] Camera moves
- [ ] Box rotates (script runs)

WebXR Ready:
- [ ] Imports added
- [ ] WebXR initialized
- [ ] Session requested
- [ ] Controllers detected
- [ ] Fallback for non-XR

## Scene Files Issue

Current: Assets in `client/assets/example.scene/`
Needed: Scene in `public/scene/`

Solution: Copy during build or update loader path

## Performance Settings

Already Optimized:
- High precision floats
- Antialias enabled
- GPU acceleration

For XR:
- May need to reduce shadow quality
- Disable expensive post-processing
- Implement LOD for meshes

## Architecture Pattern

```
React Component (page.tsx)
    ↓
Babylon Engine
    ↓
Scene
    ├── Havok Physics
    ├── Meshes with Scripts
    ├── Lights & Shadows
    └── Camera
```

## Render Loop

```
Component Mount
    ↓
Engine.runRenderLoop
    ├── scene.render()
    ├── Script updates (onUpdate)
    └── Physics simulation
    ↓
Every Frame (60+fps)
```

## Next Steps

1. Add WebXR imports to page.tsx
2. Initialize WebXRExperienceHelper in handleLoad
3. Add controller features
4. Create XR interaction scripts
5. Test on device

## Notes

- All imports are modular (tree-shakeable)
- Physics required for physics-enabled meshes
- Scripts auto-execute via scriptsMap registry
- Canvas is full-screen responsive
- No UI framework (plain Babylon.js)
- TypeScript decorators enabled
