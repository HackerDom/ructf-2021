import {JsonObject, JsonProperty} from "json2typescript";
import {FunctionConverter} from "../../Utilities/Converters";

@JsonObject("Track")
export class Track {
    @JsonProperty("notes", String, false)
    notes: string = "";

    @JsonProperty("play", FunctionConverter, true)
    play = () => {
        return 1;
    }
}