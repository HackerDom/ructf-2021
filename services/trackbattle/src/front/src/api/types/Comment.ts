import {JsonObject, JsonProperty} from "json2typescript";

@JsonObject("Comment")
export class Comment {
    @JsonProperty("id", String, true)
    id: string = "";

    @JsonProperty("post_id", String, true)
    postId: string = "";

    @JsonProperty("author_nickname", String, false)
    author: string = "";

    @JsonProperty("publishing_date", String, false)
    publishingDate: string = "";

    @JsonProperty("description", String, true)
    description: string = "";

    @JsonProperty("likes_amount", Number, false)
    likes_amount: number = 0;

    @JsonProperty("track", String, false)
    track: string = "";
}

@JsonObject("CommentResponse")
export class CommentResponse {
    @JsonProperty("track", String, false)
    track: string = "";

    @JsonProperty("description", String, false)
    description: string = "";

    @JsonProperty("post_id", String, false)
    post_id: string = "";
}