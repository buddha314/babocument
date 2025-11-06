# Project Asset Structure - Babocument

**Generated:** 2025-11-06
**Purpose:** Comprehensive guide to understanding asset organization and determining optimal Blender/GLB workflow

## 1. Current Directory Layout

### Root Structure
```
babocument/
├── .claude/                 # Claude Code settings
├── .git/                    # Git repository
├── .gitignore              # Git ignore rules
├── README.md               # Main project documentation
├── client/                 # Next.js + BabylonJS application
├── data/                   # Research data and references
├── server/                 # Backend (not yet implemented)
└── specs/                  # Project specifications
```

### Client Layer Structure
```
client/
├── .bjseditor/             # BabylonJS Editor project files and cache
├── assets/                 # Static assets directory (PRIMARY ASSET LOCATION)
│   ├── example.scene/      # BabylonJS Editor-generated scene
│   ├── albedo.png          # Texture resource
│   ├── amiga.jpg           # Texture resource
│   ├── country.env         # HDR environment texture
│   ├── cube.material       # BabylonJS material definition
│   ├── floor.material      # BabylonJS material definition
│   └── README.md           # Assets documentation (minimal)
├── public/                 # Next.js public static files
├── src/
│   ├── app/
│   │   └── page.tsx        # Main scene loading component
│   └── scripts/            # BabylonJS scene scripts
├── node_modules/          # NPM dependencies (not committed)
├── package.json
├── project.bjseditor      # BabylonJS Editor project metadata
├── tsconfig.json
└── README.md
```

## 2. Existing Documentation About Assets

### Key Documentation Found

**Main Project README**
- Mentions "Blender integration for 3D assets" in Integration Layer
- References MCP (Model Context Protocol) for Blender
- Lists 3D laboratory equipment as key feature

**Project Status & Tasks**
- Phase 3: "Client - Virtual Environment" needs 3D corridor
- Phase 4: "Librarian Character" requires 3D model, rigging, animations
- Status shows these are NOT YET STARTED

**Assets README**
- Very minimal: "This folder contains all the assets used in the project"

## 3. Existing .blend and .glb Files

### Search Results: NONE FOUND

No Blender source files or GLB/GLTF exports currently exist in the repository.

What exists instead:
- BabylonJS Editor project structure (editor native format)
- Example scene with procedurally created geometries
- Material and texture files for the example scene

## 4. Static Assets Storage Locations

### Primary Location: `/client/assets/`

Current contents:
- `example.scene/` - BabylonJS Editor scene with full hierarchy
- Material files: `cube.material`, `floor.material`
- Textures: `albedo.png`, `amiga.jpg`
- HDR environment: `country.env`

### Secondary Location: `/client/public/`

Currently minimal - just SVG logos. This is the Next.js static files directory.

### Asset Loading Mechanism

From `page.tsx`:
```typescript
await loadScene("/scene/", "example.babylon", scene, scriptsMap, {
    quality: "high",
});
```

Expects `.babylon` file in `/public/scene/` directory.

From `config.json`:
```json
"environmentTexture": {
    "url": "assets/country.env"
}
```

Can reference both `assets/` and `public/` paths.

## 5. Configuration Files Indicating Asset Organization

### BabylonJS Editor Project File
```json
{
    "version": "5.1.1",
    "lastOpenedScene": "/assets/example.scene",
    "compressedTexturesEnabled": false,
    "compressedTexturesEnabledInPreview": false
}
```

Shows editor uses `/assets/example.scene` as standard location.

### .gitignore Indicators
```
# Babylon.js Editor
*.babylon
*.glb.tmp
*.gltf.tmp
assets/generated/
```

Indicates project expects:
- Babylon files to be generated (not committed)
- Temporary GLB/GLTF files during export
- A generated assets directory

### Next.js Configuration
```javascript
webpack: (config) => {
    config.module.rules.push({
        test: /\.fx?$/,
        loader: "raw-loader"
    });
    return config;
}
```

Supports shader files in project.

## 6. Recommended Asset Structure for Blender Workflow

### Directory Organization

```
client/assets/
├── README.md                          # Update this with asset guide
├── example.scene/                     # Keep: Editor scenes
├── blender/                           # NEW: Blender source files
│   ├── librarian/
│   │   └── librarian_character.blend
│   ├── equipment/
│   │   ├── bioreactor.blend
│   │   ├── centrifuge.blend
│   │   └── incubator.blend
│   ├── environment/
│   │   ├── file_room_corridor.blend
│   │   └── year_partition.blend
│   └── exported/                      # NEW: Exported GLB files
│       ├── librarian_character.glb
│       ├── equipment/
│       └── environment/
├── materials/
├── textures/
└── environments/
```

### Alternative: Public Directory for Models

If GLB files are large or need better caching:

```
client/public/
├── models/                            # NEW: 3D models
│   ├── librarian_character.glb
│   ├── equipment/
│   └── environment/
└── textures/
```

## Key Findings Summary

1. **No Blender infrastructure exists yet** - This is intentional, project is in planning
2. **Asset directory structure is ready** - `/client/assets/` is properly organized
3. **BabylonJS Editor is the active tool** - Scene created/managed in editor
4. **Git is configured for future GLB exports** - gitignore shows awareness
5. **Scene loading expects babylon or glb formats** - Proper infrastructure in place
6. **Two approaches available**:
   - Store GLB in `/client/assets/` alongside other assets
   - Store GLB in `/client/public/` for static serving

## Recommendations

1. Create `/client/assets/blender/` for source Blender files
2. Create `/client/assets/blender/exported/` for GLB exports
3. Consider `/client/public/models/` if file sizes are large
4. Document naming conventions and organization in updated `/client/assets/README.md`
5. Update `.gitignore` to exclude `.blend` files (they're binary and large)
6. Use BabylonJS Editor to import and integrate GLB files into scenes
