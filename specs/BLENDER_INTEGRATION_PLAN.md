# Blender Integration Plan for Babocument

**Created:** 2025-11-06

## Quick Start Summary

The Babocument project is ready for Blender integration. Create these directories:

```
client/assets/blender/          (for Blender source files)
client/assets/blender/exported/ (for GLB exports)
client/public/models/           (for web serving)
```

**For detailed workflow instructions, see:** [docs/BLENDER_WORKFLOW.md](docs/BLENDER_WORKFLOW.md)

## Recommended Directory Structure

### Blender Sources (Assets Directory)

```
client/assets/blender/
├── librarian/
│   └── librarian_character_v1.blend
├── equipment/
│   ├── bioreactor.blend
│   ├── centrifuge.blend
│   ├── fermenter.blend
│   └── incubator.blend
├── environment/
│   ├── file_room_corridor.blend
│   ├── year_partition.blend
│   └── lab_workstation.blend
└── exported/
    ├── librarian_character_v1.glb
    ├── equipment/
    └── environment/
```

### Public Models Directory (for Web)

```
client/public/models/
├── librarian_character_v1.glb
├── equipment/
│   ├── bioreactor.glb
│   ├── centrifuge.glb
│   ├── fermenter.glb
│   └── incubator.glb
└── environment/
    ├── file_room_corridor.glb
    ├── year_partition.glb
    └── lab_workstation.glb
```

## Git Configuration

Update `.gitignore` to exclude Blender files (binary, large):

```
# Blender files
*.blend
*.blend1
.blend_file_history/
blender_crash_log.txt

# Generated exports (regenerated from Blender)
client/assets/blender/exported/
client/public/models/
```

## Export Settings from Blender

When exporting GLB files, use these settings:
- Format: GLB (Binary)
- Include Animations: YES
- Include Materials: YES
- Include Textures: YES (or bake into GLB)
- Export Armature: YES (for rigged characters)
- Export Shape Keys: YES (for morphs)

## Naming Convention

Use format: `[category]_[name]_v[version].glb`

Examples:
- `librarian_character_v1.glb`
- `equipment_bioreactor_v1.glb`
- `environment_corridor_v1.glb`

## Integration with BabylonJS

The current scene loading already supports GLB files.

Loading in TypeScript:
```typescript
import SceneLoader from "@babylonjs/core/Loading/sceneLoader";

SceneLoader.ImportMesh(
    "", 
    "/models/", 
    "librarian_character_v1.glb", 
    scene, 
    (meshes) => {
        console.log("Loaded:", meshes);
    }
);
```

## BabylonJS Editor Integration

1. Open BabylonJS Editor (configured at `project.bjseditor`)
2. Import GLB file (right-click scene > Import Meshes)
3. Position and configure in scene
4. Editor saves reference in scene structure
5. Export scene for application

## Update Asset Documentation

Replace `/client/assets/README.md` with expanded documentation:

```markdown
# Assets Directory

Contains all static assets and Blender source files.

## Structure
- `example.scene/` - BabylonJS Editor scenes
- `blender/` - Blender sources and exported GLB models
- `materials/` - Material definitions
- `textures/` - Image textures

## Naming: [category]_[name]_v[version].glb

For Blender integration details, see BLENDER_INTEGRATION_PLAN.md
```

## Implementation Checklist

- [ ] Create `/client/assets/blender/` directories
- [ ] Create `/client/public/models/` directories
- [ ] Update `.gitignore` for Blender files
- [ ] Update `/client/assets/README.md`
- [ ] Create Blender project template
- [ ] Begin Librarian character model
- [ ] Test GLB export and import workflow
- [ ] Integrate first character into BabylonJS scene

## Key Decisions

1. **Source Location**: `/client/assets/blender/` - keeps organization clear
2. **Export Format**: GLB (binary, efficient, single-file)
3. **Web Serving**: Can use `/client/public/models/` or serve from `/client/assets/`
4. **Git Strategy**: Exclude .blend files (binary, large) but document workflow
5. **Integration**: Use BabylonJS Editor for scene composition

## Current Status

- BabylonJS Editor: Active and configured
- Asset directories: Ready for use
- Scene loading: Supports GLB files natively
- No Blender files yet: This is the starting point

## Related Documentation

- [BLENDER_WORKFLOW.md](docs/BLENDER_WORKFLOW.md) - Detailed contributor guide for Blender export
- [PROJECT_ASSET_STRUCTURE.md](PROJECT_ASSET_STRUCTURE.md) - Complete project structure analysis
- [TASKS.md](specs/TASKS.md) - Phase-specific asset requirements
