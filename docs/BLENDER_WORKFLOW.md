# Blender Workflow Guide for Babocument Contributors

**Last Updated:** 2025-11-06

## Overview

This guide explains how to work with Blender files in the Babocument project and properly export them for use with BabylonJS.

## File Organization

### Directory Structure

```
babocument/
├── client/
│   ├── assets/
│   │   └── blender/                    # Blender source files (.blend)
│   │       ├── librarian/
│   │       ├── equipment/
│   │       ├── environment/
│   │       └── exported/               # Exported GLB files
│   └── public/
│       └── models/                     # Production GLB files (web serving)
│           ├── librarian_character_v1.glb
│           ├── equipment/
│           └── environment/
```

### File Types

- **`.blend`** - Blender source files (NOT committed to git due to size)
- **`.glb`** - Exported binary GLTF files for BabylonJS (production ready)
- **`.gltf`** - Text-based GLTF (optional, for debugging)

## Blender Export Settings

### Step-by-Step Export Process

1. **File > Export > glTF 2.0**

2. **Format Settings:**
   - Format: **glTF Binary (.glb)** ✓
   - Copyright: (optional)
   - Remember Export Settings: ✓

3. **Include Settings:**
   - Selected Objects: (based on needs)
   - Custom Properties: ✓
   - Cameras: (if needed for scene)
   - Punctual Lights: (if needed)

4. **Transform Settings:**
   - +Y Up: ✓ (BabylonJS standard)

5. **Geometry Settings:**
   - Apply Modifiers: ✓
   - UVs: ✓
   - Normals: ✓
   - Tangents: ✓
   - Vertex Colors: ✓
   - Materials: Export (✓)
   - Images: Automatic
   - Compression: Disabled (unless file size is critical)

6. **Animation Settings:**
   - Use Current Frame: (uncheck if exporting animations)
   - Animations: ✓
   - Limit to Playback Range: (check for specific clips)
   - Sampling Rate: 1
   - Always Sample Animations: (check for complex rigs)
   - NLA Strips: ✓
   - Shape Keys: ✓
   - Shape Key Normals: ✓
   - Shape Key Tangents: ✓
   - Skinning: ✓

### Critical Settings for BabylonJS

- **Format:** Must be GLB (binary) for best performance
- **+Y Up:** Required for correct orientation in BabylonJS
- **Apply Modifiers:** Essential for correct geometry
- **Materials:** Must be exported with textures
- **Skinning:** Required for rigged characters

## Naming Conventions

### File Naming Format

```
[category]_[name]_v[version].blend
[category]_[name]_v[version].glb
```

### Examples

**Blender Sources:**
- `librarian_character_v1.blend`
- `equipment_bioreactor_v2.blend`
- `environment_corridor_v1.blend`

**Exported GLB:**
- `librarian_character_v1.glb`
- `equipment_bioreactor_v2.glb`
- `environment_corridor_v1.glb`

### Version Increments

- Increment version when making significant changes
- Keep old versions if needed for rollback
- Document changes in commit messages

## Workflow Steps

### 1. Create Blender File

```bash
# Create in appropriate category
client/assets/blender/librarian/librarian_character_v1.blend
```

### 2. Model, Texture, Rig

- Follow project art style guidelines
- Keep polygon count reasonable for real-time rendering
- Use PBR materials (Principled BSDF)
- Ensure proper UV unwrapping

### 3. Export to GLB

```bash
# Export from Blender to:
client/assets/blender/exported/librarian_character_v1.glb
```

### 4. Copy to Public Directory

```bash
# Copy for web serving
cp client/assets/blender/exported/librarian_character_v1.glb \
   client/public/models/librarian_character_v1.glb
```

### 5. Test in BabylonJS

```typescript
import { SceneLoader } from "@babylonjs/core/Loading/sceneLoader";

SceneLoader.ImportMesh(
    "",                              // Import all meshes
    "/models/",                      // Base path
    "librarian_character_v1.glb",    // Filename
    scene,
    (meshes) => {
        console.log("Loaded meshes:", meshes);
        // Configure mesh properties
    }
);
```

### 6. Commit Changes

```bash
# Only commit the GLB file, not the .blend source
git add client/public/models/librarian_character_v1.glb
git commit -m "Add librarian character model v1"
```

## Git Configuration

### What Gets Committed

✓ **DO commit:**
- `.glb` files in `client/public/models/`
- Documentation updates
- Configuration files

✗ **DO NOT commit:**
- `.blend` files (binary, large)
- `.blend1` backup files
- `client/assets/blender/exported/` (regenerated)

### .gitignore Setup

```gitignore
# Blender source files
*.blend
*.blend1
.blend_file_history/
blender_crash_log.txt

# Temporary exports
client/assets/blender/exported/

# Optional: Exclude public models if using CDN
# client/public/models/
```

## Asset Requirements by Phase

### Phase 4: Librarian Character
- **Librarian Character Model**
  - Rigged for animation
  - Facial blend shapes for expressions
  - Animations: idle, gesture, walk, interact
  - Poly count: < 20k triangles

### Phase 7: Virtual Labs
- **Equipment Models:**
  - Bioreactor
  - Centrifuge
  - Fermenter
  - Incubator
  - Lab bench
  - Microscope
  - Poly count: < 5k triangles each

### Phase 3: Environment
- **File Room Elements:**
  - Corridor sections (modular)
  - Glass partitions
  - Document cards/panels
  - Floor, walls, ceiling sections

## Troubleshooting

### Model appears rotated incorrectly
- Ensure "+Y Up" is enabled in export settings
- Check axis orientation in Blender before export

### Textures missing
- Set "Images: Automatic" in export settings
- Ensure textures are packed into .blend file
- Use relative paths for texture files

### Animations not working
- Check "Animations" is enabled
- Verify armature is properly rigged
- Ensure "Skinning" is enabled
- Sample rate should be 1 for most cases

### File size too large
- Enable compression in export settings
- Reduce texture resolution
- Optimize mesh topology
- Consider using texture atlases

### Materials look wrong in BabylonJS
- Use Principled BSDF shader in Blender
- Avoid complex shader nodes
- Test with simple materials first
- Check BabylonJS material compatibility

## Best Practices

1. **Keep it Organized:** Follow directory structure strictly
2. **Version Control:** Increment versions for significant changes
3. **Document Changes:** Note material/rig/animation changes
4. **Test Early:** Import to BabylonJS frequently during development
5. **Optimize First:** Keep polygon counts low from the start
6. **PBR Materials:** Use Principled BSDF for consistent look
7. **Modular Design:** Create reusable components
8. **Backup Sources:** Keep .blend files backed up externally (not in git)

## Resources

- [BabylonJS GLTF Documentation](https://doc.babylonjs.com/features/featuresDeepDive/importers/glTF)
- [Khronos glTF 2.0 Specification](https://www.khronos.org/gltf/)
- [Blender GLTF Export Manual](https://docs.blender.org/manual/en/latest/addons/import_export/scene_gltf2.html)

## Questions?

For questions about the Blender workflow or asset requirements, see:
- [BLENDER_INTEGRATION_PLAN.md](../BLENDER_INTEGRATION_PLAN.md) - Setup and planning
- [PROJECT_ASSET_STRUCTURE.md](../PROJECT_ASSET_STRUCTURE.md) - Current structure
- [TASKS.md](../specs/TASKS.md) - Phase-specific asset requirements
