export type Note = "C" | "C#" | "D" | "D#" | "E" | "F" | "F#" | "G" | "G#" | "A" | "A#" | "B";
export type Waveform = "sine" | "square" | "sawtooth" | "triangle";
export const Waveforms = ["sine", "square", "sawtooth", "triangle"];

export class AudioPlayer {
    public static readonly Notes: Note[] = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"];
    public static readonly NoteTable: {[key in Note]: number} = {
        ["C"]: 66.0,
        ["C#"]: 69.93,
        ["D"]: 74.08,
        ["D#"]: 78.49,
        ["E"]: 83.16,
        ["F"]: 88.10,
        ["F#"]: 93.34,
        ["G"]: 98.89,
        ["G#"]: 104.77,
        ["A"]: 111.00,
        ["A#"]: 117.60,
        ["B"]: 124.59
    };

    private Stop: boolean;

    private AudioContext: AudioContext;
    private MainGainNode: GainNode;

    public constructor() {
        this.AudioContext = new AudioContext();
        this.AudioContext.resume();

        this.MainGainNode = this.AudioContext.createGain();
        this.MainGainNode.connect(this.AudioContext.destination);
        this.MainGainNode.gain.value = 5;
        this.Stop = false;
    }

    public stopPlaying(): void {
        this.Stop = true;
    }

    public async playString(music: string, type: Waveform): Promise<void> {
        const notes: Note[] = [];
        for (let i = 0; i < music.length; i++){
            if (i < music.length - 1){
                if (music[i+1] === "#"){
                    notes.push(music.slice(i,i+1) as Note);
                    i++;
                } else {
                    notes.push(music[i] as Note);
                }
            } else {
                notes.push(music[i] as Note);
            }
        }
        await this.play(notes, type);
    }

    public async play(music: Note[], type: Waveform): Promise<void> {
        this.Stop = false;
        for (let i of music) {
            if (this.Stop){
                break;
            }
            const a = this.playTone(AudioPlayer.NoteTable[i], type);
            const delay = (millis: number) => new Promise<void>((resolve, reject) => {
                setTimeout(() => resolve(), millis)
            });
            await delay(400);
            a.stop();
        }
    }

    public async playNote(note: Note, type: Waveform): Promise<void> {
        const a = this.playTone(AudioPlayer.NoteTable[note], type);
        const delay = (millis: number) => new Promise<void>((resolve, reject) => {
            setTimeout(() => resolve(), millis)
        });
        await delay(400);
        a.stop();
    }

    private playTone (freq: number, type: Waveform) {
        let osc = this.AudioContext.createOscillator();
        osc.connect(this.MainGainNode);
        osc.type = Waveforms.some(x => x === type) ? type : "triangle";

        osc.frequency.value = freq;
        osc.start();

        return osc;
    }
}