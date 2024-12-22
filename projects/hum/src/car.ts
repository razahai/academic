import * as THREE from "three";
import { loadGLTFAsync, logLoadingAction } from "./utils";
import { Timeline } from "./timeline";

export class Car {
    model!: THREE.Group;
    driverSeat!: THREE.Object3D;
    passengerSeat!: THREE.Object3D;
    copyPos!: boolean;
    
    isRunning: boolean;
    t: number;
    speed: number;

    constructor() {
        this.isRunning = false;
        this.t = 0;
        this.speed = 0.0015;
    }

    async init() {
        this.model = (await loadGLTFAsync("models/car.glb", (progress) => logLoadingAction(`Loading car model... ${(progress.loaded / progress.total * 100).toFixed(0)}%`))).scene;
        this.model.position.set(-1580.381, 7.161, -1092.738);
        this.copyPos = false;
        
        this.model.traverse((object) => {
            if (object.name === "driver") 
                this.driverSeat = object;
            else if (object.name === "passenger")
                this.passengerSeat = object;
        });
    }

    update(timeline: Timeline, path: THREE.CatmullRomCurve3) {
        if (!this.isRunning) return;

        if (this.copyPos) {
            this.passengerSeat.getWorldPosition(timeline.cameraLocation);
        }

        this.t += this.speed;
        if (this.t >= 1) { 
            // car has reached end of path 
            this.isRunning = false;
            this.t = 0;
            return;
        }

        const pos = path.getPointAt(1 - this.t);
        this.model.position.copy(pos);

        // look at the point in front of current pos 
        const tAhead = this.t - 0.01 >= 0 ? (this.t - 0.01) % 1 : 0; // this % but might be pointless
        const posAhead = path.getPointAt(1 - tAhead);
        
        this.model.lookAt(posAhead);
    }
}