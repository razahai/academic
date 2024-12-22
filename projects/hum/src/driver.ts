import * as THREE from "three";
import { GLTF } from 'three/addons/loaders/GLTFLoader.js';
import { loadGLTFAsync, logLoadingAction } from "./utils";

export class Driver {
    model!: THREE.Group;
    mixer!: THREE.AnimationMixer;
    animations!: THREE.AnimationClip[];
    currentAnim!: THREE.AnimationAction;
    
    async init() {
        const glb: GLTF = (await loadGLTFAsync("models/driver.glb", (progress) => logLoadingAction(`Loading driver model... ${(progress.loaded / progress.total * 100).toFixed(0)}%`)));
        this.model = glb.scene;

        this.animations = glb.animations;
        this.mixer = new THREE.AnimationMixer(this.model); 
    }

    animate(animName: string) {
        if (!this.currentAnim) {
            const anim = this.mixer.clipAction(THREE.AnimationClip.findByName(this.animations, animName));
            this.currentAnim = anim;
            this.currentAnim.play();
            return;
        } 

        if (this.currentAnim.getClip().name === animName) 
            return;

        const anim = this.mixer.clipAction(THREE.AnimationClip.findByName(this.animations, animName));
    
        if (this.currentAnim.isRunning()) {
            this.currentAnim.fadeOut(0.3);
            anim.reset();
            anim.fadeIn(0.3);
            anim.play();
        } else {
            anim.play();
        }

        this.currentAnim = anim;
    }
}