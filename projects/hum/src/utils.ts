import { GLTF, GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { AudioManager } from "./audio";
import { Timeline } from "./timeline";

const modelLoader = new GLTFLoader();

export let delays: (() => void)[] = [];

export async function loadGLTFAsync(model: string, progCB?: (progress: ProgressEvent) => void): Promise<GLTF> {
    return new Promise((resolve, reject) => {
        modelLoader.load(
            model, 
            (glb) => resolve(glb),
            progCB || undefined,
            reject
        )
    })
}

export function toggleTransition(delay: number) {
    const transitionScreen = document.getElementsByClassName("transition")[0];

    transitionScreen.classList.toggle("fade-in");
    // disgusting but it's fine
    delays.push(new (setDelay as any)(() => { 
        transitionScreen.classList.toggle("fade-in");
    }, delay));
}

export function togglePreface(delay: number) {
    const transitionScreen = document.getElementsByClassName("transition")[0] as HTMLElement;

    // remove banner fake loading text
    (document.getElementsByClassName("banner")[0] as HTMLElement).innerHTML = "";
    transitionScreen.innerText = "The following setting is intended to depict D.C, regardless of whether it is accurate or not.";
    transitionScreen.classList.toggle("fade-in");
    delays.push(new (setDelay as any)(() => {
        transitionScreen.classList.toggle("fade-in");
        (document.getElementsByClassName("banner")[0] as HTMLElement).style.display = "none";
        transitionScreen.innerText = "";
    }, delay));
}

export function toggleChapter(delay: number, chapter: string) {
    const transitionScreen = document.getElementsByClassName("transition")[0] as HTMLElement;

    transitionScreen.innerText = chapter;
    transitionScreen.style.backgroundColor = "transparent";
    transitionScreen.classList.toggle("fade-in");
    transitionScreen.style.fontSize = "2em";
    transitionScreen.style.fontWeight = "600";

    delays.push(new (setDelay as any)(() => {
        transitionScreen.classList.toggle("fade-in");
        transitionScreen.innerText = "";
    }, delay));
    // do this after since it'll look weird if it suddenly turns black while fading
    delays.push(new (setDelay as any)(() => {
        transitionScreen.style.backgroundColor = "black";
        transitionScreen.style.fontSize = "1em";
        transitionScreen.style.fontWeight = "normal";
    }, delay + 1000));
}


export function toggleImage(delay: number, imagePath: string) {
    const imageScreen = document.getElementsByClassName("image")[0];
    
    (imageScreen.children[0] as HTMLImageElement).src = imagePath;
    
    (imageScreen.children[0] as HTMLImageElement).onload = () => {
        imageScreen.classList.toggle("fade-in");
        delays.push(new (setDelay as any)(() => {
            imageScreen.classList.toggle("fade-in");
        }, delay));
    }
}

export function toggleCitation(delay: number, citation: string) {
    const citationBox = document.getElementsByClassName("citation")[0];
    
    (citationBox as HTMLDivElement).innerText = citation;

    citationBox.classList.toggle("fade-in");
    delays.push(new (setDelay as any)(() => {
        citationBox.classList.toggle("fade-in");
    }, delay));
}

export function toggleEnd() {
    const transitionScreen = document.getElementsByClassName("transition")[0] as HTMLElement;

    // end credits hardcoded lmao
    transitionScreen.innerText = "<p><b>End</b><br><br><br>Thanks,<br><br><b>Ms. AnLo & Mr. Weinberg</b> for being great teachers<br><b>GTA San Andreas</b> for the 3D models<br><b>Lud and Schlatt Crossing</b> for background music<br>...and all of the research in the Works Cited<br><br><br>:)</p>";
    transitionScreen.classList.toggle("fade-in");
}

export function disableEventsOOF(audioManager: AudioManager, timeline: Timeline) {
    // this is really cursed ts but i don't have time
    audioManager.pauseCurrent();

    for (const delay of delays) {
        (delay as any).pause();
    }

    if (timeline.actionDelayedTime !== undefined && timeline.currentAction.delay) {
        const dateThen = timeline.actionDelayedTime - timeline.currentAction.delay; // Date.now()
        timeline.delayedRemaining = timeline.currentAction.delay - (Date.now() - dateThen); // delay - current elapsed
    }

    if (timeline.actionTransitionTime !== undefined && timeline.currentAction.data) {
        let transitionData = undefined;
        
        for (const data of timeline.currentAction.data) {
            if (data.type === "transition")
                transitionData = data;
        }

        if (transitionData) {
            const dateThen = timeline.actionTransitionTime - transitionData.delay; // Date.now()
            timeline.transitionRemaining = transitionData.delay - (Date.now() - dateThen); // delay - current elapsed
        }
    }
}

export function enableEventsOOF(audioManager: AudioManager, timeline: Timeline) {
    audioManager.resumeCurrent();

    for (const delay of delays) {
        (delay as any).resume();
    }

    if (timeline.actionDelayedTime !== undefined && timeline.delayedRemaining) {
        timeline.actionDelayedTime = Date.now() + timeline.delayedRemaining; // append remaining to current time
    }
    
    if (timeline.actionTransitionTime !== undefined && timeline.transitionRemaining) {
        timeline.actionTransitionTime =  Date.now() + timeline.transitionRemaining; 
    }
}

export function logLoadingAction(action: string) {
    const logDisplay = document.getElementById("loading-log") as HTMLElement;
    if (!logDisplay) return;

    logDisplay.innerText = action;
}

export const setDelay = function(this: any, callback: () => void, delay: number) {
    // setTimeout with pause and resume ability
    // stolen from https://stackoverflow.com/questions/3969475/javascript-pause-settimeout
    let timeout: any, start: number, remaining: number = delay;

    this.pause = () => {
        window.clearTimeout(timeout);
        timeout = null;
        remaining -= Date.now() - start;
    };

    this.resume = function() {
        if (timeout) {
            return;
        }

        start = Date.now();
        timeout = window.setTimeout(() => {
            callback();

            // self removal
            const tIndex = delays.indexOf(this);
            if (tIndex !== -1) {
                delays.splice(tIndex, 1);
            }
        }, remaining);
    };

    this.resume();
}