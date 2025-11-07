"use client";

import { useEffect, useRef } from "react";

import { Scene } from "@babylonjs/core/scene";
import { Engine } from "@babylonjs/core/Engines/engine";
import { Vector3 } from "@babylonjs/core/Maths/math.vector";
import { SceneLoaderFlags } from "@babylonjs/core/Loading/sceneLoaderFlags";
import { HavokPlugin } from "@babylonjs/core/Physics/v2/Plugins/havokPlugin";

import HavokPhysics from "@babylonjs/havok";

import "@babylonjs/core/Loading/loadingScreen";
import "@babylonjs/core/Loading/Plugins/babylonFileLoader";

import "@babylonjs/core/Cameras/universalCamera";

import "@babylonjs/core/Meshes/groundMesh";

import "@babylonjs/core/Lights/directionalLight";
import "@babylonjs/core/Lights/Shadows/shadowGeneratorSceneComponent";

import "@babylonjs/core/Materials/PBR/pbrMaterial";
import "@babylonjs/core/Materials/standardMaterial";

// WebXR imports
import { WebXRDefaultExperience } from "@babylonjs/core/XR/webXRDefaultExperience";
import "@babylonjs/core/XR/features/WebXRDepthSensing";
import "@babylonjs/core/Helpers/sceneHelpers";

import "@babylonjs/core/Rendering/depthRendererSceneComponent";
import "@babylonjs/core/Rendering/prePassRendererSceneComponent";

import "@babylonjs/core/Materials/Textures/Loaders/envTextureLoader";

import "@babylonjs/core/Physics";

import "@babylonjs/materials/sky";

import { loadScene } from "babylonjs-editor-tools";

/**
 * We import the map of all scripts attached to objects in the editor.
 * This will allow the loader from `babylonjs-editor-tools` to attach the scripts to the
 * loaded objects (scene, meshes, transform nodes, lights, cameras, etc.).
 */
import { scriptsMap } from "@/scripts";
import ApiTest from "@/components/ApiTest";

export default function Home() {
	const canvasRef = useRef<HTMLCanvasElement>(null);

	useEffect(() => {
		if (!canvasRef.current) {
			return;
		}

		const engine = new Engine(canvasRef.current, true, {
			stencil: true,
			antialias: true,
			audioEngine: true,
			adaptToDeviceRatio: true,
			disableWebGL2Support: false,
			useHighPrecisionFloats: true,
			powerPreference: "high-performance",
			failIfMajorPerformanceCaveat: false,
		});

		const scene = new Scene(engine);

		handleLoad(engine, scene);

		let listener: () => void;
		window.addEventListener("resize", listener = () => {
			engine.resize();
		});

		return () => {
			scene.dispose();
			engine.dispose();

			window.removeEventListener("resize", listener);
		};
	}, [canvasRef]);

	async function handleLoad(engine: Engine, scene: Scene) {
		const havok = await HavokPhysics();
		scene.enablePhysics(new Vector3(0, -981, 0), new HavokPlugin(true, havok));

		// Import necessary classes
		const { MeshBuilder, StandardMaterial, Color3, Texture, ArcRotateCamera, HemisphericLight } = await import("@babylonjs/core");

		// Create camera
		const camera = new ArcRotateCamera("camera", -Math.PI / 2, Math.PI / 3, 10, new Vector3(0, 1, 0), scene);
		camera.attachControl();
		scene.activeCamera = camera;

		// Create lighting
		const light = new HemisphericLight("light", new Vector3(0, 1, 0), scene);
		light.intensity = 0.7;

		// Create ground
		const ground = MeshBuilder.CreateGround("ground", { width: 10, height: 10 }, scene);
		const groundMaterial = new StandardMaterial("groundMaterial", scene);
		groundMaterial.diffuseColor = new Color3(0.3, 0.3, 0.4);
		ground.material = groundMaterial;

		// Create a textured box
		const box = MeshBuilder.CreateBox("box", { size: 2 }, scene);
		box.position.y = 1;
		const boxMaterial = new StandardMaterial("boxMaterial", scene);
		
		// Try to load the texture, fallback to color if it fails
		try {
			boxMaterial.diffuseTexture = new Texture("/assets/amiga.jpg", scene);
		} catch (error) {
			console.warn("Failed to load texture, using solid color:", error);
			boxMaterial.diffuseColor = new Color3(0.8, 0.4, 0.2);
		}
		box.material = boxMaterial;

		// Add some rotation animation
		scene.registerBeforeRender(() => {
			box.rotation.y += 0.01;
		});

		console.log("Scene created successfully");

		if (scene.activeCamera) {
			scene.activeCamera.attachControl();
		}

		// Initialize WebXR with default experience
		try {
			const xrHelper = await WebXRDefaultExperience.CreateAsync(scene, {
				floorMeshes: scene.meshes.filter((mesh) => mesh.name.toLowerCase().includes("ground") || mesh.name.toLowerCase().includes("floor")),
				// Optional: Configure teleportation
				optionalFeatures: true,
			});

			console.log("WebXR initialized successfully");

			// Log when entering/exiting XR
			xrHelper.baseExperience.onStateChangedObservable.add((state) => {
				console.log("WebXR state changed:", state);
			});
		} catch (error) {
			console.warn("WebXR not supported or failed to initialize:", error);
		}

		engine.runRenderLoop(() => {
			scene.render();
		});
	}

	return (
		<main className="flex w-screen h-screen flex-col items-center justify-between">
			<canvas
				ref={canvasRef}
				className="w-full h-full outline-none select-none"
			/>
			<ApiTest />
		</main>
	);
}
