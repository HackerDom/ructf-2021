import {JsonObject, JsonProperty} from "json2typescript";

@JsonObject("User")
export class User {
    @JsonProperty("username", String, false)
    username: string = "";

    @JsonProperty("password_sha256", String, false)
    password_sha256: string = "";
}