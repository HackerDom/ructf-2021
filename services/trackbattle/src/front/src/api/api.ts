import {User} from "./types/User";
import {JsonSerializer} from "../Utilities/JsonSerializer";
import {Track} from "./types/Track";
import {CookiesStorage} from "../Utilities/CookiesStorage";
import {Post} from "./types/Post";
import {Comment, CommentResponse} from "./types/Comment";

export interface Result<R> {
    data: R | null;
    statusCode: number;
    error?: string;
}

export class api {
    private static readonly baseUrl: string = `//${window.location.host}/api`;
    private static readonly authHeader = "XTBAuth";
    private static readonly contentTypeHeader = "Content-Type";

    public static async fetch<R>(url: string, request: RequestInit): Promise<Result<R>> {
        try {
            const result = await fetch(this.baseUrl + url, request);
            if (result.ok) {
                const data = await result.json();

                if (!data.status || data.status === "success") {
                    return {data: data, statusCode: result.status};
                }
                return {data: null, statusCode: data.message};
            }

            const data = await result.json();

            return {data: null, statusCode: result.status, error: data.message}
        } catch (e) {
            return {data: null, statusCode: 500, error: e};
        }
    }

    public static async createUser(user: User): Promise<Result<{ auth_token: string }>> {
        const request: RequestInit = {
            method: "POST",
            body: JSON.stringify(JsonSerializer.serialize<User>(user, User)),
            headers: {[this.contentTypeHeader]: "application/json"}
        };
        return await this.fetch<{ auth_token: string }>("/users", request);
    }

    public static async getUser(): Promise<Result<{nickname: string, payment_info: string, posts: string[]}>> {
        const request: RequestInit = {
            method: "GET",
            headers: {[this.authHeader]: CookiesStorage.getAuth() || ""}
        };
        return await this.fetch<{nickname: string, payment_info: string, posts: string[]}>("/users", request);
    }

    public static async loginUser(user: User): Promise<Result<{ auth_token: string }>> {
        const request: RequestInit = {
            method: "PUT",
            body: JSON.stringify(JsonSerializer.serialize<User>(user, User)),
            headers: {[this.contentTypeHeader]: "application/json"}
        };
        return await this.fetch<{ auth_token: string }>("/users/auth_token", request);
    }

    public static async getLatest(): Promise<Result<{ posts: string[] }>> {
        const request: RequestInit = {
            method: "GET",
            headers: {[this.authHeader]: CookiesStorage.getAuth() || ""}
        };
        return this.fetch<{ posts: string[] }>("/posts/latest?limit=50", request)
    }

    public static async getMyPosts(): Promise<Result<{ post_ids: string[] }>> {
        const request: RequestInit = {
            method: "GET",
            headers: {[this.authHeader]: CookiesStorage.getAuth() || ""}
        };
        return this.fetch<{ post_ids: string[] }>("/posts/my", request)
    }

    public static async getPost(postId: string): Promise<Result<Post>> {
        const request: RequestInit = {
            method: "GET",
            headers: {[this.authHeader]: CookiesStorage.getAuth() || ""}
        };
        const result = await this.fetch<Post>(`/posts/${postId}`, request);

        return {data: result.data ? JsonSerializer.deserialize(result.data, Post) : result.data, error: result.error, statusCode: result.statusCode }
    }

    public static async postTrack(data: Track) {
        const request: RequestInit = {
            method: "POST",
            body: JSON.stringify(JsonSerializer.serialize<Track>(data, Track)),
            headers: {
                [this.contentTypeHeader]: "application/json",
                [this.authHeader]: CookiesStorage.getAuth() || "",
            }
        };
        return this.fetch("/posts", request)
    }

    public static async getComment(commentId: string): Promise<Result<Comment>> {
        const request: RequestInit = {
            method: "GET",
            headers: {[this.authHeader]: CookiesStorage.getAuth() || ""}
        };
        const result = await this.fetch<Comment>(`/comments/${commentId}`, request);

        return {data: result.data ? JsonSerializer.deserialize(result.data, Comment) : result.data, error: result.error, statusCode: result.statusCode }
    }

    public static async addComment(data: CommentResponse): Promise<Result<void>> {
        const request: RequestInit = {
            method: "POST",
            body: JSON.stringify(JsonSerializer.serialize<CommentResponse>(data, CommentResponse)),
            headers: {
                [this.contentTypeHeader]: "application/json",
                [this.authHeader]: CookiesStorage.getAuth() || "",
            }
        };
        return this.fetch("/comments", request)
    }

    public static async likePost(postId: string): Promise<Result<void>> {
        const request: RequestInit = {
            method: "PUT",
            headers: {[this.authHeader]: CookiesStorage.getAuth() || ""}
        };
        return this.fetch(`/posts/${postId}`, request)
    }

    public static async likeComment(commentId: string): Promise<Result<void>> {
        const request: RequestInit = {
            method: "PUT",
            headers: {[this.authHeader]: CookiesStorage.getAuth() || ""}
        };
        return this.fetch(`/comments/${commentId}`, request)
    }

}
