import {JsonObject, JsonProperty} from "json2typescript";
import {FunctionConverter} from "../../Utilities/Converters";
import {AudioPlayer} from "../../Utilities/AudioPlayer";

@JsonObject("Track")
export class Track {
    @JsonProperty("title", String, true)
    title: string = "";

    @JsonProperty("description", String, false)
    description: string = "";

    @JsonProperty("track", String, false)
    notes: string = "";

    @JsonProperty("play", FunctionConverter, true)
    play = async (player: AudioPlayer) => {
        player.stopPlaying();
        await player.playString(this.notes)
    }
}