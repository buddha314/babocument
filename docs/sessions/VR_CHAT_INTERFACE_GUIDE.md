# VR Chat Interface & Immersive VR Application Guide

**Created:** November 6, 2025  
**Purpose:** Implementation guide for creating in-world 3D chat screens and immersive VR experiences in Babylon.js

---

## Table of Contents

1. [3D Chat Screen Implementation](#3d-chat-screen-implementation)
2. [Immersive VR Application Development](#immersive-vr-application-development)
3. [Integration Patterns](#integration-patterns)
4. [Implementation Examples](#implementation-examples)
5. [Best Practices & Performance](#best-practices--performance)

---

## 3D Chat Screen Implementation

### Overview

Creating a chat interface inside a 3D scene requires rendering UI elements as textures on 3D meshes. Babylon.js provides the **GUI system** (`@babylonjs/gui`) with two primary approaches:

1. **AdvancedDynamicTexture (ADT) - 3D Mode**: Renders GUI on mesh surfaces in world space
2. **AdvancedDynamicTexture - Fullscreen Mode**: Overlay on entire screen (for desktop)

For VR chat screens, use **3D Mode** to place interactive panels in the world.

---

### Strategy: 3D GUI Panel in World Space

#### Key Components

**AdvancedDynamicTexture.CreateForMesh()**
- Creates a texture that renders GUI controls
- Applies to any mesh (plane, sphere, curved surface)
- Resolution independent
- Supports full event handling (click, hover, input)

**GUI Controls for Chat:**
- `Rectangle`: Container for chat UI
- `StackPanel`: Vertical layout for messages
- `TextBlock`: Display chat messages
- `InputText`: User text input
- `Button`: Send button
- `ScrollViewer`: Scrollable message history

---

### Basic Implementation

```typescript
import { Scene, MeshBuilder, Vector3, StandardMaterial, Color3 } from "@babylonjs/core";
import { AdvancedDynamicTexture, Rectangle, StackPanel, TextBlock, InputText, Button, ScrollViewer, Control } from "@babylonjs/gui";

class ChatPanel3D {
  private mesh: BABYLON.Mesh;
  private advancedTexture: AdvancedDynamicTexture;
  private messageContainer: StackPanel;
  private scrollViewer: ScrollViewer;
  private inputText: InputText;
  private messages: string[] = [];

  constructor(scene: Scene, position: Vector3) {
    // Create plane mesh for the screen
    this.mesh = MeshBuilder.CreatePlane("chatScreen", {
      width: 4,
      height: 3,
      sideOrientation: BABYLON.Mesh.DOUBLESIDE
    }, scene);
    
    this.mesh.position = position;
    
    // Make the panel emit light so it's visible in dark scenes
    const material = new StandardMaterial("chatMaterial", scene);
    material.emissiveColor = new Color3(0.2, 0.2, 0.2);
    this.mesh.material = material;

    // Create GUI texture with high resolution for crisp text
    this.advancedTexture = AdvancedDynamicTexture.CreateForMesh(
      this.mesh,
      1024,  // Width resolution
      768    // Height resolution
    );

    this.createChatUI();
  }

  private createChatUI() {
    // Main container
    const mainContainer = new Rectangle("mainContainer");
    mainContainer.width = "100%";
    mainContainer.height = "100%";
    mainContainer.thickness = 0;
    mainContainer.background = "rgba(20, 20, 40, 0.95)";
    mainContainer.cornerRadius = 10;
    this.advancedTexture.addControl(mainContainer);

    // Title bar
    const titleBar = new Rectangle("titleBar");
    titleBar.width = "100%";
    titleBar.height = "60px";
    titleBar.verticalAlignment = Control.VERTICAL_ALIGNMENT_TOP;
    titleBar.thickness = 0;
    titleBar.background = "rgba(50, 100, 200, 0.9)";
    mainContainer.addControl(titleBar);

    const titleText = new TextBlock("title", "Chat with Agent");
    titleText.color = "white";
    titleText.fontSize = 24;
    titleText.fontWeight = "bold";
    titleBar.addControl(titleText);

    // Scrollable message area
    this.scrollViewer = new ScrollViewer("messageScroll");
    this.scrollViewer.width = "95%";
    this.scrollViewer.height = "580px";
    this.scrollViewer.top = "70px";
    this.scrollViewer.verticalAlignment = Control.VERTICAL_ALIGNMENT_TOP;
    this.scrollViewer.thickness = 1;
    this.scrollViewer.color = "rgba(100, 100, 100, 0.5)";
    mainContainer.addControl(this.scrollViewer);

    // Message container (stack panel)
    this.messageContainer = new StackPanel("messageStack");
    this.messageContainer.width = "100%";
    this.messageContainer.verticalAlignment = Control.VERTICAL_ALIGNMENT_TOP;
    this.scrollViewer.addControl(this.messageContainer);

    // Input area container
    const inputArea = new Rectangle("inputArea");
    inputArea.width = "95%";
    inputArea.height = "100px";
    inputArea.verticalAlignment = Control.VERTICAL_ALIGNMENT_BOTTOM;
    inputArea.top = "-10px";
    inputArea.thickness = 1;
    inputArea.color = "rgba(100, 100, 100, 0.5)";
    inputArea.background = "rgba(30, 30, 50, 0.9)";
    mainContainer.addControl(inputArea);

    // Text input
    this.inputText = new InputText("messageInput");
    this.inputText.width = "70%";
    this.inputText.height = "60px";
    this.inputText.left = "-80px";
    this.inputText.color = "white";
    this.inputText.background = "rgba(50, 50, 70, 0.9)";
    this.inputText.focusedBackground = "rgba(70, 70, 90, 0.9)";
    this.inputText.placeholderText = "Type your message...";
    this.inputText.placeholderColor = "rgba(200, 200, 200, 0.5)";
    this.inputText.fontSize = 18;
    this.inputText.thickness = 2;
    this.inputText.autoStretchWidth = false;
    inputArea.addControl(this.inputText);

    // Send button
    const sendButton = Button.CreateSimpleButton("sendBtn", "Send");
    sendButton.width = "120px";
    sendButton.height = "60px";
    sendButton.left = "120px";
    sendButton.color = "white";
    sendButton.background = "rgba(50, 150, 50, 0.9)";
    sendButton.fontSize = 18;
    sendButton.thickness = 2;
    inputArea.addControl(sendButton);

    // Button hover effect
    sendButton.onPointerEnterObservable.add(() => {
      sendButton.background = "rgba(70, 180, 70, 0.9)";
    });
    sendButton.onPointerOutObservable.add(() => {
      sendButton.background = "rgba(50, 150, 50, 0.9)";
    });

    // Handle send button click
    sendButton.onPointerClickObservable.add(() => {
      this.sendMessage();
    });

    // Handle Enter key in input
    this.inputText.onKeyboardEventProcessedObservable.add((eventData) => {
      if (eventData.key === "Enter") {
        this.sendMessage();
      }
    });
  }

  private sendMessage() {
    const message = this.inputText.text.trim();
    if (!message) return;

    // Add user message
    this.addMessage("You", message, "rgba(50, 100, 200, 0.3)");

    // Clear input
    this.inputText.text = "";

    // Simulate agent response (replace with actual API call)
    setTimeout(() => {
      this.addMessage("Agent", "I received your message: " + message, "rgba(100, 50, 200, 0.3)");
    }, 500);
  }

  public addMessage(sender: string, text: string, bgColor: string = "rgba(50, 50, 70, 0.5)") {
    const messageContainer = new Rectangle("msg-" + Date.now());
    messageContainer.width = "95%";
    messageContainer.height = "auto";  // Auto-height based on content
    messageContainer.thickness = 1;
    messageContainer.color = "rgba(100, 100, 100, 0.3)";
    messageContainer.background = bgColor;
    messageContainer.cornerRadius = 5;
    messageContainer.paddingTop = "10px";
    messageContainer.paddingBottom = "10px";
    messageContainer.paddingLeft = "10px";
    messageContainer.paddingRight = "10px";
    messageContainer.adaptHeightToChildren = true;

    const messageStack = new StackPanel();
    messageStack.width = "100%";
    messageStack.adaptHeightToChildren = true;
    messageContainer.addControl(messageStack);

    // Sender name
    const senderText = new TextBlock("sender", sender);
    senderText.height = "25px";
    senderText.color = "rgba(200, 200, 255, 1)";
    senderText.fontSize = 16;
    senderText.fontWeight = "bold";
    senderText.textHorizontalAlignment = Control.HORIZONTAL_ALIGNMENT_LEFT;
    messageStack.addControl(senderText);

    // Message text (word wrap enabled)
    const messageText = new TextBlock("text", text);
    messageText.color = "white";
    messageText.fontSize = 18;
    messageText.textWrapping = true;
    messageText.textHorizontalAlignment = Control.HORIZONTAL_ALIGNMENT_LEFT;
    messageText.resizeToFit = true;
    messageStack.addControl(messageText);

    this.messageContainer.addControl(messageContainer);

    // Auto-scroll to bottom
    setTimeout(() => {
      this.scrollViewer.verticalBar.value = 1;
    }, 100);
  }

  public getMesh(): BABYLON.Mesh {
    return this.mesh;
  }

  public dispose() {
    this.advancedTexture.dispose();
    this.mesh.dispose();
  }
}

// Usage in your scene
const chatPanel = new ChatPanel3D(scene, new Vector3(0, 2, 5));
```

---

### Advanced: Curved Chat Screen

For a more immersive feel, use a curved surface:

```typescript
class CurvedChatPanel extends ChatPanel3D {
  constructor(scene: Scene, position: Vector3) {
    // Create curved cylinder instead of plane
    const cylinder = MeshBuilder.CreateCylinder("curvedScreen", {
      height: 3,
      diameter: 4,
      tessellation: 24,
      arc: 0.5  // 180-degree arc
    }, scene);
    
    cylinder.position = position;
    cylinder.rotation.y = Math.PI; // Face the user

    // Rest of the setup...
  }
}
```

---

### Integration with Agent API

```typescript
class AgentChatPanel extends ChatPanel3D {
  private apiEndpoint = "http://localhost:8000/api/chat";

  private async sendMessage() {
    const message = this.inputText.text.trim();
    if (!message) return;

    this.addMessage("You", message, "rgba(50, 100, 200, 0.3)");
    this.inputText.text = "";

    try {
      const response = await fetch(this.apiEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
      });

      const data = await response.json();
      this.addMessage("Agent", data.reply, "rgba(100, 50, 200, 0.3)");
    } catch (error) {
      this.addMessage("System", "Error connecting to agent", "rgba(200, 50, 50, 0.3)");
    }
  }
}
```

---

## Immersive VR Application Development

### WebXR Overview

**WebXR Device API** enables VR and AR experiences in web browsers. Babylon.js provides comprehensive WebXR support through:

- `WebXRDefaultExperience`: Quick setup with common features
- `WebXRExperienceHelper`: Fine-grained control
- Feature modules for specific capabilities

---

### Current Project Status

Your client already has:
- ✅ Babylon.js 8.33.2 installed
- ✅ `@babylonjs/gui` package
- ✅ WebXR imports present (`WebXRDefaultExperience`, `WebXRDepthSensing`)
- ✅ Engine configured with stencil buffer (required for XR)
- ✅ Physics enabled (Havok)
- ✅ Basic WebXR initialization in `page.tsx`

---

### WebXR Implementation Levels

#### Level 1: Basic VR (Current Implementation)

Your `page.tsx` already includes basic WebXR:

```typescript
const xrHelper = await WebXRDefaultExperience.CreateAsync(scene, {
  floorMeshes: scene.meshes.filter(mesh => 
    mesh.name.toLowerCase().includes("ground") || 
    mesh.name.toLowerCase().includes("floor")
  ),
  optionalFeatures: true,
});
```

This provides:
- ✅ VR mode toggle button
- ✅ Controller tracking
- ✅ Basic pointer selection
- ✅ Teleportation

#### Level 2: Enhanced VR Features

Add more immersive features:

```typescript
import { WebXRExperienceHelper } from "@babylonjs/core/XR/webXRExperienceHelper";
import { WebXRControllerPointerSelection } from "@babylonjs/core/XR/features/WebXRControllerPointerSelection";
import { WebXRMotionControllerTeleportation } from "@babylonjs/core/XR/features/WebXRMotionControllerTeleportation";
import { WebXRHandTracking } from "@babylonjs/core/XR/features/WebXRHandTracking";
import { WebXRNearInteraction } from "@babylonjs/core/XR/features/WebXRNearInteraction";

async function setupEnhancedVR(scene: Scene) {
  const xrHelper = await WebXRDefaultExperience.CreateAsync(scene, {
    floorMeshes: [ground],
    disableTeleportation: false,
  });

  const xr = xrHelper.baseExperience;

  // Controller pointer selection
  const pointerSelection = xr.featuresManager.enableFeature(
    WebXRControllerPointerSelection,
    "stable",
    {
      xrInput: xr.input,
      enablePointerSelectionOnAllControllers: true
    }
  );

  // Teleportation with custom snap points
  const teleportation = xr.featuresManager.enableFeature(
    WebXRMotionControllerTeleportation,
    "stable",
    {
      xrInput: xr.input,
      floorMeshes: [ground],
      snapPositions: [
        new Vector3(0, 0, 0),
        new Vector3(5, 0, 5),
        new Vector3(-5, 0, 5)
      ]
    }
  );

  // Hand tracking (Quest 2+, Quest Pro)
  try {
    const handTracking = xr.featuresManager.enableFeature(
      WebXRHandTracking,
      "latest",
      {
        xrInput: xr.input,
        jointMeshes: {
          enablePhysics: true
        }
      }
    );

    console.log("Hand tracking enabled");
  } catch (e) {
    console.log("Hand tracking not available:", e);
  }

  // Near interaction (touching objects)
  const nearInteraction = xr.featuresManager.enableFeature(
    WebXRNearInteraction,
    "stable",
    {
      xrInput: xr.input,
      farInteractionFeature: pointerSelection,
      enableNearInteractionOnAllControllers: true,
      useUtilityLayer: true
    }
  );

  return xrHelper;
}
```

#### Level 3: VR-Optimized UI

Special considerations for UI in VR:

```typescript
import { AdvancedDynamicTexture, Rectangle, TextBlock, Control } from "@babylonjs/gui";

class VROptimizedUI {
  private scene: Scene;
  private xrHelper: WebXRDefaultExperience;

  constructor(scene: Scene, xrHelper: WebXRDefaultExperience) {
    this.scene = scene;
    this.xrHelper = xrHelper;
    
    // Listen for VR state changes
    xrHelper.baseExperience.onStateChangedObservable.add((state) => {
      if (state === WebXRState.IN_XR) {
        this.setupVRUI();
      } else {
        this.setupDesktopUI();
      }
    });
  }

  private setupVRUI() {
    // In VR: Use 3D world-space UI
    const chatPanel = new ChatPanel3D(this.scene, new Vector3(0, 1.5, 3));
    
    // Make sure UI faces the camera
    this.scene.registerBeforeRender(() => {
      const camera = this.scene.activeCamera;
      if (camera) {
        chatPanel.getMesh().lookAt(camera.position);
      }
    });
  }

  private setupDesktopUI() {
    // On desktop: Use fullscreen overlay
    const advancedTexture = AdvancedDynamicTexture.CreateFullscreenUI("desktopUI");
    
    const panel = new Rectangle();
    panel.width = "400px";
    panel.height = "600px";
    panel.cornerRadius = 10;
    panel.color = "white";
    panel.thickness = 2;
    panel.background = "rgba(20, 20, 40, 0.95)";
    panel.horizontalAlignment = Control.HORIZONTAL_ALIGNMENT_RIGHT;
    panel.verticalAlignment = Control.VERTICAL_ALIGNMENT_CENTER;
    panel.left = "-20px";
    advancedTexture.addControl(panel);

    // Add chat UI to panel...
  }
}
```

---

### VR Controller Interaction

Handle controller input for grabbing and interacting:

```typescript
class VRControllerManager {
  private scene: Scene;
  private xrHelper: WebXRDefaultExperience;

  constructor(scene: Scene, xrHelper: WebXRDefaultExperience) {
    this.scene = scene;
    this.xrHelper = xrHelper;

    this.setupControllerEvents();
  }

  private setupControllerEvents() {
    const xr = this.xrHelper.baseExperience;

    // Listen for controller connection
    xr.input.onControllerAddedObservable.add((controller) => {
      console.log("Controller connected:", controller.uniqueId);

      controller.onMotionControllerInitObservable.add((motionController) => {
        // Handle different button presses
        
        // Trigger button (index finger)
        const triggerComponent = motionController.getComponent("xr-standard-trigger");
        if (triggerComponent) {
          triggerComponent.onButtonStateChangedObservable.add((component) => {
            if (component.pressed) {
              console.log("Trigger pressed");
              this.handleTriggerPress(controller);
            }
          });
        }

        // Squeeze button (grip)
        const squeezeComponent = motionController.getComponent("xr-standard-squeeze");
        if (squeezeComponent) {
          squeezeComponent.onButtonStateChangedObservable.add((component) => {
            if (component.pressed) {
              console.log("Squeeze pressed");
              this.handleGripPress(controller);
            }
          });
        }

        // Thumbstick
        const thumbstickComponent = motionController.getComponent("xr-standard-thumbstick");
        if (thumbstickComponent) {
          thumbstickComponent.onAxisValueChangedObservable.add((axes) => {
            console.log("Thumbstick:", axes.x, axes.y);
            this.handleThumbstick(axes.x, axes.y);
          });
        }

        // A/X button
        const aButton = motionController.getComponent("a-button") || 
                        motionController.getComponent("x-button");
        if (aButton) {
          aButton.onButtonStateChangedObservable.add((component) => {
            if (component.pressed) {
              console.log("A/X button pressed");
              this.handleAButtonPress();
            }
          });
        }
      });
    });
  }

  private handleTriggerPress(controller: WebXRInputSource) {
    // Example: Select/click objects
    const ray = controller.getWorldPointerRayToRef(new Ray());
    const hit = this.scene.pickWithRay(ray);
    
    if (hit?.pickedMesh) {
      console.log("Selected mesh:", hit.pickedMesh.name);
    }
  }

  private handleGripPress(controller: WebXRInputSource) {
    // Example: Grab objects
    console.log("Grab action");
  }

  private handleThumbstick(x: number, y: number) {
    // Example: Smooth locomotion
    if (Math.abs(y) > 0.1) {
      const camera = this.scene.activeCamera as WebXRCamera;
      if (camera) {
        const forward = camera.getForwardRay().direction;
        camera.position.addInPlace(forward.scale(y * 0.1));
      }
    }
  }

  private handleAButtonPress() {
    // Example: Toggle UI or menu
    console.log("Menu toggle");
  }
}
```

---

### Performance Optimization for VR

VR requires **90 FPS minimum** (Quest 2: 72-120 Hz, Quest 3: 72-120 Hz):

```typescript
class VRPerformanceOptimizer {
  private scene: Scene;
  private xrHelper: WebXRDefaultExperience;
  private lowQualityMode = false;

  constructor(scene: Scene, xrHelper: WebXRDefaultExperience) {
    this.scene = scene;
    this.xrHelper = xrHelper;

    xrHelper.baseExperience.onStateChangedObservable.add((state) => {
      if (state === WebXRState.IN_XR) {
        this.enableVROptimizations();
      } else {
        this.disableVROptimizations();
      }
    });

    this.monitorFrameRate();
  }

  private enableVROptimizations() {
    // Reduce shadow quality
    this.scene.lights.forEach(light => {
      const shadowGenerator = light.getShadowGenerator();
      if (shadowGenerator) {
        shadowGenerator.mapSize = 512; // Reduce from 1024+
        shadowGenerator.useBlurExponentialShadowMap = false;
      }
    });

    // Disable expensive post-processing
    this.scene.postProcessesEnabled = false;

    // Use LOD for complex meshes
    this.scene.meshes.forEach(mesh => {
      if (mesh.getTotalVertices() > 10000) {
        // Add LOD levels if not present
        // mesh.addLODLevel(distance, simplifiedMesh);
      }
    });

    // Reduce physics accuracy slightly
    const physicsEngine = this.scene.getPhysicsEngine();
    if (physicsEngine) {
      physicsEngine.setTimeStep(1 / 60); // From 1/90
    }

    console.log("VR optimizations enabled");
  }

  private disableVROptimizations() {
    // Restore desktop quality
    this.scene.lights.forEach(light => {
      const shadowGenerator = light.getShadowGenerator();
      if (shadowGenerator) {
        shadowGenerator.mapSize = 1024;
      }
    });

    this.scene.postProcessesEnabled = true;
  }

  private monitorFrameRate() {
    let frameCount = 0;
    let lastTime = performance.now();

    this.scene.registerBeforeRender(() => {
      frameCount++;
      const currentTime = performance.now();

      if (currentTime - lastTime >= 1000) {
        const fps = frameCount;
        frameCount = 0;
        lastTime = currentTime;

        // Auto-adjust quality based on FPS
        if (this.xrHelper.baseExperience.state === WebXRState.IN_XR) {
          if (fps < 72 && !this.lowQualityMode) {
            console.warn("Low FPS detected:", fps, "- reducing quality");
            this.enableLowQualityMode();
          } else if (fps > 85 && this.lowQualityMode) {
            console.log("FPS recovered:", fps, "- restoring quality");
            this.disableLowQualityMode();
          }
        }
      }
    });
  }

  private enableLowQualityMode() {
    this.lowQualityMode = true;
    
    // Further reduce quality
    this.scene.lights.forEach(light => {
      const shadowGenerator = light.getShadowGenerator();
      if (shadowGenerator) {
        shadowGenerator.mapSize = 256;
      }
    });

    // Reduce texture quality
    this.scene.textures.forEach(texture => {
      if (texture instanceof BABYLON.Texture) {
        texture.updateSamplingMode(BABYLON.Texture.BILINEAR_SAMPLINGMODE);
      }
    });
  }

  private disableLowQualityMode() {
    this.lowQualityMode = false;
    this.enableVROptimizations(); // Back to normal VR mode
  }
}
```

---

## Integration Patterns

### Pattern 1: Conditional UI Rendering

```typescript
class AdaptiveUIManager {
  private scene: Scene;
  private chatPanel3D?: ChatPanel3D;
  private chatPanelOverlay?: any;

  constructor(scene: Scene) {
    this.scene = scene;
  }

  async initialize(xrHelper: WebXRDefaultExperience) {
    xrHelper.baseExperience.onStateChangedObservable.add((state) => {
      if (state === WebXRState.IN_XR) {
        this.showVRUI();
      } else {
        this.showDesktopUI();
      }
    });

    // Start with desktop UI
    this.showDesktopUI();
  }

  private showVRUI() {
    // Clean up desktop UI
    if (this.chatPanelOverlay) {
      this.chatPanelOverlay.dispose();
      this.chatPanelOverlay = null;
    }

    // Create 3D world-space chat panel
    this.chatPanel3D = new ChatPanel3D(this.scene, new Vector3(0, 1.5, 3));
  }

  private showDesktopUI() {
    // Clean up VR UI
    if (this.chatPanel3D) {
      this.chatPanel3D.dispose();
      this.chatPanel3D = null;
    }

    // Create fullscreen overlay
    const adt = AdvancedDynamicTexture.CreateFullscreenUI("desktopUI");
    // Add desktop chat UI...
    this.chatPanelOverlay = adt;
  }
}
```

---

### Pattern 2: Shared Chat Logic

```typescript
interface IChatInterface {
  addMessage(sender: string, text: string, color?: string): void;
  onSendMessage(callback: (message: string) => void): void;
}

class ChatLogic {
  private messageHistory: Array<{sender: string, text: string, timestamp: Date}> = [];
  private onMessageCallback?: (message: string) => Promise<string>;

  constructor(private apiEndpoint: string) {}

  async sendMessage(message: string): Promise<string> {
    this.messageHistory.push({
      sender: "User",
      text: message,
      timestamp: new Date()
    });

    try {
      const response = await fetch(this.apiEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          message,
          history: this.messageHistory.slice(-10) // Last 10 messages
        })
      });

      const data = await response.json();
      const reply = data.reply || data.response || "No response";

      this.messageHistory.push({
        sender: "Agent",
        text: reply,
        timestamp: new Date()
      });

      return reply;
    } catch (error) {
      const errorMsg = "Error: Could not reach agent";
      this.messageHistory.push({
        sender: "System",
        text: errorMsg,
        timestamp: new Date()
      });
      return errorMsg;
    }
  }

  getHistory() {
    return [...this.messageHistory];
  }
}

// Use in both VR and desktop UIs
const chatLogic = new ChatLogic("http://localhost:8000/api/chat");

// VR panel
const vrChat = new ChatPanel3D(scene, position);
vrChat.onSend = async (msg) => {
  const reply = await chatLogic.sendMessage(msg);
  vrChat.addMessage("Agent", reply);
};

// Desktop panel
const desktopChat = new DesktopChatPanel();
desktopChat.onSend = async (msg) => {
  const reply = await chatLogic.sendMessage(msg);
  desktopChat.addMessage("Agent", reply);
};
```

---

## Implementation Examples

### Complete VR Chat Scene

```typescript
// File: client/src/lib/VRChatScene.ts

import { Scene, Vector3, HemisphericLight, MeshBuilder, StandardMaterial, Color3 } from "@babylonjs/core";
import { WebXRDefaultExperience, WebXRState } from "@babylonjs/core/XR";
import { ChatPanel3D } from "./ChatPanel3D";
import { VRControllerManager } from "./VRControllerManager";
import { VRPerformanceOptimizer } from "./VRPerformanceOptimizer";

export class VRChatScene {
  private scene: Scene;
  private xrHelper?: WebXRDefaultExperience;
  private chatPanel?: ChatPanel3D;

  constructor(scene: Scene) {
    this.scene = scene;
  }

  async initialize() {
    // Create environment
    this.createEnvironment();

    // Setup WebXR
    await this.setupWebXR();

    // Create chat interface
    this.createChatInterface();

    // Setup performance monitoring
    if (this.xrHelper) {
      new VRPerformanceOptimizer(this.scene, this.xrHelper);
    }
  }

  private createEnvironment() {
    // Lighting
    const light = new HemisphericLight("light", new Vector3(0, 1, 0), this.scene);
    light.intensity = 0.7;

    // Ground
    const ground = MeshBuilder.CreateGround("ground", {
      width: 20,
      height: 20
    }, this.scene);
    
    const groundMat = new StandardMaterial("groundMat", this.scene);
    groundMat.diffuseColor = new Color3(0.2, 0.3, 0.4);
    ground.material = groundMat;

    // Skybox
    const skybox = MeshBuilder.CreateBox("skybox", { size: 1000 }, this.scene);
    const skyboxMat = new StandardMaterial("skyboxMat", this.scene);
    skyboxMat.backFaceCulling = false;
    skyboxMat.emissiveColor = new Color3(0.1, 0.15, 0.3);
    skybox.material = skyboxMat;
  }

  private async setupWebXR() {
    try {
      this.xrHelper = await WebXRDefaultExperience.CreateAsync(this.scene, {
        floorMeshes: this.scene.meshes.filter(m => m.name === "ground"),
        optionalFeatures: true,
      });

      console.log("WebXR initialized");

      // Setup controller interactions
      new VRControllerManager(this.scene, this.xrHelper);

      // Monitor VR state
      this.xrHelper.baseExperience.onStateChangedObservable.add((state) => {
        console.log("XR State:", WebXRState[state]);
        
        if (state === WebXRState.IN_XR) {
          this.onEnterVR();
        } else if (state === WebXRState.NOT_IN_XR) {
          this.onExitVR();
        }
      });
    } catch (error) {
      console.warn("WebXR not available:", error);
    }
  }

  private createChatInterface() {
    // Position chat panel in front of spawn point
    this.chatPanel = new ChatPanel3D(this.scene, new Vector3(0, 1.5, 3));

    // Make chat panel always face the user
    this.scene.registerBeforeRender(() => {
      if (this.scene.activeCamera && this.chatPanel) {
        this.chatPanel.getMesh().lookAt(this.scene.activeCamera.position);
      }
    });
  }

  private onEnterVR() {
    console.log("Entered VR mode - optimizations active");
    // VR-specific adjustments handled by VRPerformanceOptimizer
  }

  private onExitVR() {
    console.log("Exited VR mode - restored desktop quality");
  }

  dispose() {
    if (this.chatPanel) {
      this.chatPanel.dispose();
    }
  }
}

// Usage in page.tsx
async function handleLoad(engine: Engine, scene: Scene) {
  // ... physics setup ...

  const vrChatScene = new VRChatScene(scene);
  await vrChatScene.initialize();

  engine.runRenderLoop(() => {
    scene.render();
  });
}
```

---

## Best Practices & Performance

### 1. Text Rendering in VR

**Problem:** Small text is hard to read in VR

**Solutions:**
- Use minimum font size of 24px for body text
- Use 32px+ for headings
- Increase line spacing (1.5x minimum)
- Use high-contrast colors (white on dark background)
- Increase texture resolution for GUI (1024x768 minimum, 2048x1536 for crisp text)

```typescript
const advancedTexture = AdvancedDynamicTexture.CreateForMesh(
  mesh,
  2048,  // High resolution for crisp text
  1536
);
```

### 2. Panel Positioning

**Optimal viewing distance:** 1.5 - 3 meters  
**Optimal height:** Eye level (1.4 - 1.7 meters)  
**Optimal angle:** Perpendicular to user or slightly curved

```typescript
// Good positioning
const chatPanel = new ChatPanel3D(scene, new Vector3(0, 1.5, 2.5));

// Auto-position based on user head
function positionPanelInFrontOfUser(camera: Camera, distance: number = 2.5) {
  const forward = camera.getForwardRay().direction;
  const position = camera.position.add(forward.scale(distance));
  position.y = 1.5; // Fixed height
  return position;
}
```

### 3. Interaction Feedback

Always provide visual/haptic feedback for interactions:

```typescript
button.onPointerDownObservable.add(() => {
  // Visual feedback
  button.scaleX = 0.95;
  button.scaleY = 0.95;
  
  // Haptic feedback (if controller available)
  const xrInput = xrHelper?.baseExperience.input;
  if (xrInput) {
    xrInput.controllers.forEach(controller => {
      controller.motionController?.pulse(0.5, 100); // 50% intensity, 100ms
    });
  }
});

button.onPointerUpObservable.add(() => {
  button.scaleX = 1.0;
  button.scaleY = 1.0;
});
```

### 4. Memory Management

Dispose resources when switching modes:

```typescript
class ResourceManager {
  private resources: Array<{ dispose: () => void }> = [];

  register(resource: any) {
    if (resource && typeof resource.dispose === 'function') {
      this.resources.push(resource);
    }
  }

  disposeAll() {
    this.resources.forEach(r => r.dispose());
    this.resources = [];
  }
}
```

### 5. Testing Checklist

**Desktop Testing:**
- [ ] Scene renders correctly
- [ ] Chat UI appears and is interactive
- [ ] Messages send and receive
- [ ] Scroll works properly
- [ ] Text is readable

**VR Testing:**
- [ ] VR mode enters successfully
- [ ] Controllers are tracked
- [ ] Can point at UI elements
- [ ] Can type with virtual keyboard
- [ ] Chat panel is readable
- [ ] Teleportation works
- [ ] Performance maintains >72 FPS
- [ ] Exit VR cleanly

**Cross-Device Testing:**
- [ ] Meta Quest 2
- [ ] Meta Quest 3 / Pro
- [ ] PSVR2
- [ ] PC VR (SteamVR)

---

## Device Compatibility

### Supported Devices

| Device | WebXR Support | Features Available |
|--------|---------------|-------------------|
| Meta Quest 2/3/Pro | ✅ Native | Controllers, Hand tracking, Passthrough |
| PlayStation VR2 | ✅ Native | Controllers, Eye tracking |
| HoloLens 2 | ✅ Native | Hand tracking, AR |
| Windows Mixed Reality | ✅ Via Edge/Chrome | Controllers |
| PC VR (SteamVR) | ✅ Via Chrome | Controllers |
| Pico Neo 3 | ✅ Native | Controllers |

### Browser Requirements

- **Chrome/Edge:** Best support, recommended
- **Firefox:** Good support
- **Safari:** Limited WebXR support (iOS)

**HTTPS Required:** WebXR only works on secure connections (https:// or localhost)

---

## Next Steps

### Immediate Implementation (Next Session)

1. **Create Chat Panel Component**
   - Implement `ChatPanel3D.ts` class
   - Add to existing scene in `page.tsx`
   - Test in desktop mode

2. **Enhance VR Experience**
   - Add controller event handling
   - Implement VR performance monitoring
   - Add VR/desktop mode switching

3. **Connect to Agent API**
   - Integrate with existing `/api/chat` endpoint
   - Add streaming response support
   - Handle connection errors gracefully

4. **Test on Target Devices**
   - Deploy to HTTPS server (required for VR)
   - Test on Meta Quest 3
   - Verify performance (>72 FPS)

### Future Enhancements

- Voice input for VR (Web Speech API)
- Gesture-based controls
- Multi-user VR chat rooms
- Spatial audio for agent responses
- Avatar representation
- Document visualization in 3D space
- AR mode for mobile devices

---

## Resources

### Official Documentation
- [Babylon.js GUI Documentation](https://doc.babylonjs.com/features/featuresDeepDive/gui/gui)
- [Babylon.js WebXR Documentation](https://doc.babylonjs.com/features/featuresDeepDive/webXR/introToWebXR)
- [WebXR Device API Specification](https://www.w3.org/TR/webxr/)
- [Meta Quest Development](https://developer.oculus.com/documentation/web/webxr-getting-started/)

### Babylon.js Playground Examples
- [GUI Examples](https://playground.babylonjs.com/#XCPP9Y)
- [WebXR Examples](https://playground.babylonjs.com/#PPM311)
- [VR Controller Input](https://playground.babylonjs.com/#EZDVEF)

### Related Project Files
- `client/src/app/page.tsx` - Main scene setup
- `WEBXR_IMPLEMENTATION_GUIDE.txt` - WebXR overview
- `docs/PLOTLY_BABYLONJS_INTEGRATION.md` - Visualization patterns

---

## Troubleshooting

### Issue: Chat text is blurry in VR

**Solution:** Increase texture resolution
```typescript
const advancedTexture = AdvancedDynamicTexture.CreateForMesh(mesh, 2048, 1536);
```

### Issue: UI not responding to clicks in VR

**Solution:** Ensure pointer selection is enabled
```typescript
const pointerSelection = xr.featuresManager.enableFeature(
  WebXRControllerPointerSelection,
  "stable"
);
```

### Issue: Low frame rate in VR

**Solution:** Enable automatic quality adjustment
```typescript
new VRPerformanceOptimizer(scene, xrHelper);
```

### Issue: WebXR not available

**Possible causes:**
- Not using HTTPS (use localhost or deploy to HTTPS)
- Browser doesn't support WebXR
- Device not connected or recognized
- WebXR flags disabled in browser

---

**End of Guide**

*This document provides comprehensive implementation details for creating immersive VR chat experiences in Babylon.js. Use as reference for next development session.*
