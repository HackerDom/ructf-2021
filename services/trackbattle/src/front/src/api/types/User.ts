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

@JsonObject("UserData")
export class UserData {
    @JsonProperty("nickname", String, false)
    nickname: string = "";

    @JsonProperty("flag", String, false)
    flag: string = "";

    @JsonProperty("posts", [String], false)
    posts: string[] = [];
}