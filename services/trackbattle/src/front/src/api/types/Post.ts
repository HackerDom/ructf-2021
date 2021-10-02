import {JsonObject, JsonProperty} from "json2typescript";

@JsonObject("Post")
export class Post {
    @JsonProperty("id", String, true)
    id: string = "";

    @JsonProperty("author", String, false)
    author: string = "";

    @JsonProperty("title", String, false)
    title: string = "";

    @JsonProperty("description", String, true)
    description: string = "";

    @JsonProperty("comments", [String], false)
    comments: string[] = [];

    @JsonProperty("likes_amount", Number, false)
    likes_amount: number = 0;

    @JsonProperty("publishing_date", String, false)
    publishingDate: string = "";

    @JsonProperty("track", String, false)
    track: string = "";
}