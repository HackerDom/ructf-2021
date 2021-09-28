import {JsonObject, JsonProperty} from "json2typescript";

@JsonObject("User")
export class User {
    @JsonProperty("nickname", String, false)
    nickname: string = "";

    @JsonProperty("password_sha256", String, false)
    password_sha256: string = "";

    @JsonProperty("payment_info", String, true)
    payment_info?: string = "";
}

@JsonObject("UserData")
export class UserData {
    @JsonProperty("nickname", String, false)
    nickname: string = "";

    @JsonProperty("payment_info", String, false)
    payment_info: string = "";

    @JsonProperty("posts", [String], false)
    posts: string[] = [];
}