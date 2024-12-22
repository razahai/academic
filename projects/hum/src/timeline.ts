import * as THREE from "three";
import { Car } from "./car";
import { Driver } from "./driver";
import { paths } from "./paths";
import { 
    toggleTransition, 
    togglePreface, 
    toggleChapter, 
    toggleImage, 
    toggleCitation,
    toggleEnd
} from "./utils";
import { AudioManager } from "./audio";

interface TimelineAction {
    id: number;
    name: string;
    path?: string;
    speed?: number;
    anim?: string;
    camera?: "passenger" | [number, number, number];
    delay?: number;
    data?: ActionData[];
    audio?: "background" | string;
}

interface ActionData {
    type: "transition" | "image" | "citation";
    transition?: string;
    chapter?: string;
    image?: string;
    lookat?: [number, number, number];
    citation?: string;
    delay: number;
}

export class Timeline {
    actions: TimelineAction[];
    currentAction: TimelineAction;
    actionTransitionTime: number | undefined;
    transitionRemaining: number | undefined;
    actionDelayedTime: number | undefined;
    delayedRemaining: number | undefined;
    cameraLocation: THREE.Vector3;
    audioManager: AudioManager;
    isPlaying: boolean;

    car: Car;
    driver: Driver;
    camera: THREE.PerspectiveCamera;
    clock: THREE.Clock;

    constructor(car: Car, driver: Driver, camera: THREE.PerspectiveCamera, audioManager: AudioManager) {
        this.actions = [];
        this.currentAction = { id: -1, name: "start" };
        this.car = car;
        this.driver = driver;
        this.camera = camera;
        this.clock = new THREE.Clock();
        this.actionTransitionTime = undefined;
        this.actionDelayedTime = undefined;
        this.cameraLocation = this.camera.position.clone();
        this.audioManager = audioManager;
        this.isPlaying = true;

    }

    async init(): Promise<void> {
        const response = await fetch("timeline.json");
        const data = await response.json();
        
        for (const action of data.timeline) {
            this.actions.push(action);
        }
    }

    update(): void {
        if (!this.isPlaying) return;
        this.driver.mixer.update(this.clock.getDelta());

        if (!this.cameraLocation.equals(this.camera.position)) {
            // spaghetti code but crunch time so ...
            if (this.currentAction.data) {
                let transitionData: ActionData | undefined = undefined;

                for (const data of this.currentAction.data) {
                    if (data.type === "transition")
                        transitionData = data;
                }

                if (transitionData) {
                    setTimeout(() => {
                        this.camera.position.copy(this.cameraLocation);
                        if (transitionData.lookat)
                            this.camera.lookAt(new THREE.Vector3(transitionData.lookat[0], transitionData.lookat[1], transitionData.lookat[2]));        
                    }, 1250);
                } else {
                    this.camera.position.copy(this.cameraLocation);
                }
            }  else {
                this.camera.position.copy(this.cameraLocation);
            }
        }

        if (!this.car.isRunning) {
            // add delay _after_ path runs
            if (this.currentAction.delay && !this.actionDelayedTime) {
                this.actionDelayedTime = Date.now() + this.currentAction.delay;
            }
        }

        if (this.isActionCompleted()) {
            if (this.currentAction.id + 1 >= this.actions.length)
                return;

            this.actionDelayedTime = undefined;
            this.actionTransitionTime = undefined;
            this.logAction(this.currentAction, "finished! iterating actions...");

            this.currentAction = this.actions[this.currentAction.id + 1];
            this.logAction(this.currentAction, "starting...");
            
            if (this.currentAction.name === "end") {
                this.isPlaying = false;
                toggleEnd();
                return;
            }

            if (this.currentAction.speed)
                this.car.speed = this.currentAction.speed;    
            // since path is in action, we need car to allow path following
            if (this.currentAction.path) 
                this.car.isRunning = true;
            if (this.currentAction.anim)
                this.driver.animate(this.currentAction.anim);

            if (this.currentAction.camera) {
                if (typeof this.currentAction.camera === "string") {
                    this.car.copyPos = true;
                    this.car.passengerSeat.getWorldPosition(this.cameraLocation);
                } else {
                    this.camera.position.set(this.currentAction.camera[0], this.currentAction.camera[1], this.currentAction.camera[2]);
                }
                // don't infinitely run this
                this.currentAction.camera = undefined;
            }

            if (this.currentAction.audio)
                this.audioManager.play(this.currentAction.audio);

            if (this.currentAction.data)
                this.handleActionData();
        }

        if (this.currentAction.path) // if path exists, run path following
            this.car.update(this, paths[this.currentAction.path as keyof typeof paths]);
    }

    logAction(action: TimelineAction, status: string): void {
        // (id) [name] - status
        if (action.id === -1) 
            // hardcode status for starting action
            console.info(`(${action.id}) [${action.name}] - video init .`);
        else
            console.info(`(${action.id}) [${action.name}] - ${status}`);
    }

    handleActionData() {
        if (!this.currentAction.data) return;
    
        for (const data of this.currentAction.data) {
            switch (data.type) {
                case "transition":
                    this.actionTransitionTime = Date.now() + (data.delay);
                    if (data.transition === "preface") {
                        togglePreface(data.delay);
                    } else if (data.transition === "chapter" && data.chapter) {
                        toggleChapter(data.delay, data.chapter);
                    } else {
                        toggleTransition(data.delay);
                    }
                    break;
                case "image":
                    if (!data.image) return; 
                    toggleImage(data.delay, `/img/${data.image}`);
                    break;
                case "citation":
                    if (!data.citation) return;
                    toggleCitation(data.delay, data.citation);
                    break;
            }
        }
    }

    isActionCompleted(): boolean {
        if (
            (!this.car.isRunning) && // car has stopped path
            (!this.actionDelayedTime || Date.now() > this.actionDelayedTime) // overall delay has finished
        ) {
            if (this.currentAction.data) { // data specific checks
                if (
                    (!this.actionTransitionTime || Date.now() > this.actionTransitionTime) && // possible transition delay has finished
                    (!document.getElementsByClassName("image")[0].classList.contains("fade-in")) && // possible image delay has finished
                    (!document.getElementsByClassName("citation")[0].classList.contains("fade-in")) // possible citation delay has finished
                ) {
                    return true;
                } else {
                    return false;
                }
            } else {
                return true;
            }
        }
        return false;
    }
}