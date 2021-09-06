import {JsonObject, JsonProperty} from "json2typescript";
import {FunctionConverter} from "../../Utilities/Converters";
import {AudioPlayer, Note} from "../../Pages/TrackPage/AudioPlayer";

@JsonObject("Track")
export class Track {
    @JsonProperty("notes", String, false)
    notes: string = "";

    @JsonProperty("play", FunctionConverter, true)
    play = async () => {
        await this.player.play(this.notes.split("") as Note[])
    }

    player: AudioPlayer = new AudioPlayer();
}