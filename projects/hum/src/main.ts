import * as THREE from 'three';
import { PointerLockControls } from 'three/addons/controls/PointerLockControls.js';
import { Sky } from 'three/addons/objects/sky.js';
import { Car } from "./car";
import { Driver } from "./driver";
import { Timeline } from './timeline';
import { AudioManager } from "./audio";
import { 
	disableEventsOOF,
	enableEventsOOF,
	loadGLTFAsync, 
	logLoadingAction 
} from "./utils";

let timeline: Timeline;
let renderer: THREE.WebGLRenderer;
let camera: THREE.PerspectiveCamera;
let scene: THREE.Scene;
let initialLockIn: boolean;
let focused: boolean;

async function init() {
	// init scene
	scene = new THREE.Scene();
	camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 750);

	// init renderer
	renderer = new THREE.WebGLRenderer();
	renderer.setSize(window.innerWidth, window.innerHeight);

	document.body.appendChild(renderer.domElement);
	window.addEventListener("resize", () => {
		camera.aspect = window.innerWidth / window.innerHeight;
		camera.updateProjectionMatrix();
		
		renderer.setSize(window.innerWidth, window.innerHeight);
	});

	// init light
	const light = new THREE.AmbientLight(0xffd6c9);
	scene.add(light);

	// init sky
	const sky: Sky = new Sky();
	sky.scale.setScalar(450000);
	scene.add(sky);

	sky.material.uniforms.mieCoefficient.value = 0.005;
	sky.material.uniforms.mieDirectionalG.value = 0.7;

	const sun = new THREE.Vector3();

	const phi = THREE.MathUtils.degToRad(0);
	const theta = THREE.MathUtils.degToRad(180);

	sun.setFromSphericalCoords(1, phi, theta);
	sky.material.uniforms.sunPosition.value.copy(sun);

	scene.fog = new THREE.Fog(0xcccccc, 200, 300);

	// init controls
	const controls = new PointerLockControls(camera, renderer.domElement);
	document.addEventListener("click", () => { 
		if (!controls.isLocked) {
			focused = true;
			controls.lock();
			// add fake loading screen just so people don't think it's broken
			if (!initialLockIn) {
				(document.getElementsByClassName("banner")[0] as HTMLElement).innerHTML = "<div class=\"loader\"></div><p id=\"loading-log\"></p>";
				initialLockIn = true; // just so people don't tab back and fwd to bypass clicking in the beginning
			}
		}
	});

	// init map
	logLoadingAction("Loading map model...");
	const map = (await loadGLTFAsync("models/map.glb", (progress) => logLoadingAction(`Loading map model... ${(progress.loaded / progress.total * 100).toFixed(0)}%`))).scene;
    camera.position.set(-1518, 8.504, -927.83);
	scene.add(map);

	// init models
	logLoadingAction("Loading car model...");
	const car = new Car();
	await car.init();
	scene.add(car.model);

	logLoadingAction("Loading driver model...");
	const driver = new Driver();
	await driver.init();
	car.driverSeat.add(driver.model);

	// init audio
	logLoadingAction("Loading audio...");
	const audioManager = new AudioManager();
	await audioManager.init();

	// init timeline
	logLoadingAction("Loading timeline...");
	timeline = new Timeline(car, driver, camera, audioManager);
	await timeline.init();

	// out of focus events
	window.addEventListener("blur", () => {
		disableEventsOOF(audioManager, timeline);
		focused = false;
	});
	window.addEventListener("focus", () => {
		enableEventsOOF(audioManager, timeline);
		focused = true;
	});
}

function animate() {
	requestAnimationFrame(animate);

	if (initialLockIn && focused && timeline.isPlaying) 
		timeline.update();

	renderer.render(scene, camera);
}

init().then(() => animate());