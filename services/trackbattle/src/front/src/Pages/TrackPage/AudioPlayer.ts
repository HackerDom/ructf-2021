export type Note = "C" | "C#" | "D" | "D#" | "E" | "F" | "F#" | "G" | "G#" | "A" | "A#" | "B";

export class AudioPlayer {
    private static readonly NoteTable: {[key in Note]: number} = {
        ["C"]: 66.0, // до
        ["C#"]: 69.93,
        ["D"]: 74.08,// ре
        ["D#"]: 78.49,
        ["E"]: 83.16,// ми
        ["F"]: 88.10,// фа
        ["F#"]: 93.34,
        ["G"]: 98.89,// соль
        ["G#"]: 104.77,
        ["A"]: 111.00,// ля
        ["A#"]: 117.60,
        ["B"]: 124.59// си
    };

    private AudioContext: AudioContext;
    private MainGainNode: GainNode;

    public constructor() {
        this.AudioContext = new AudioContext();
        this.AudioContext.resume();

        this.MainGainNode = this.AudioContext.createGain();
        this.MainGainNode.connect(this.AudioContext.destination);
        this.MainGainNode.gain.value = 5;
    }

    public async play(music: Note[]): Promise<void> {
        for (let i of music) {
            const a = this.playTone(AudioPlayer.NoteTable[i]);
            const delay = (millis: number) => new Promise<void>((resolve, reject) => {
                setTimeout(_ => resolve(), millis)
            });
            await delay(400);
            a.stop();
        }
    }

    private playTone (freq: number) {
        let osc = this.AudioContext.createOscillator();
        osc.connect(this.MainGainNode);
        osc.type = "triangle";

        osc.frequency.value = freq;
        osc.start();

        return osc;
    }
}