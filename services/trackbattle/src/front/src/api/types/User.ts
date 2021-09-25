import {JsonObject, JsonProperty} from "json2typescript";

@JsonObject("User")
export class User {
    @JsonProperty("nickname", String, false)
    nickname: string = "";

    @JsonProperty("password_sha256", String, false)
    password_sha256: string = "";

    @JsonProperty("flag", String, true)
    flag?: string = "";
}