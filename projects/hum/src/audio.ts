import { logLoadingAction } from "./utils";

interface HUMAudios {
    [key: string]: HTMLAudioElement;
}

export class AudioManager {
    currentAudio: HTMLAudioElement | undefined;
    backgroundAudio: HTMLAudioElement | undefined;
    // preload all audios so since reqing will take too long
    audios: HUMAudios;
    // i don't know a better way to do this, the site is completely client side so it won't have access to the /public/audio folder
    amtAudios: number = 27;
    

    constructor() {
        this.audios = {};
        this.currentAudio = undefined;
        this.backgroundAudio = undefined;
    }

    async init() {
        for (let i = 1; i <= this.amtAudios; i++) {
            const audioName = `audio_${i}`;
            logLoadingAction(`Loading ${audioName}...`);
            this.audios[audioName] = new Audio(`audio/${audioName}.mov`);
            this.audios[audioName].addEventListener("ended", () => {
                console.log(`(audio) ${audioName} ended.`);
                if (this.currentAudio == this.audios[audioName]) {
                    this.currentAudio = undefined;
                }
            })
        }

        logLoadingAction(`Loading background music...`);
        const mediaElement = new Audio("audio/background.mp3");
        mediaElement.volume = 0.1;
        mediaElement.loop = true;
        this.audios["background"] = mediaElement;
    }

    play(audio: string) {
        if (audio === "background") {
            // keep this in diff var since currentAudio and backgroundAudio run simultaneously
            this.backgroundAudio = this.audios["background"];
            this.backgroundAudio.play();
        } else {
            this.currentAudio = this.audios[audio];
            this.audios[audio].play();
        }
    }

    pause(audio: string) {
        this.audios[audio].pause();
    }

    resumeCurrent() {
        if (this.currentAudio && this.currentAudio.paused)
            this.currentAudio.play();
        if (this.backgroundAudio && this.backgroundAudio.paused)
            this.backgroundAudio.play();
    }

    pauseCurrent() {
        if (this.currentAudio && !this.currentAudio.paused)
            this.currentAudio.pause();
        if (this.backgroundAudio && !this.backgroundAudio.paused)
            this.backgroundAudio.pause();
    }
}