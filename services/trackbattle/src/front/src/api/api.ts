import {User} from "./types/User";
import {JsonSerializer} from "../Utilities/JsonSerializer";

export interface Result<R> {
    data: R | null;
    statusCode: number;
    error?: string;
}

export class api {
    private static readonly baseUrl: string = "http://localhost:5000/api";
    private static readonly authHeader = "XTBAuth";
    private static readonly contentTypeHeader = "Content-Type";

    public static async fetch<R>(url: string, request: RequestInit): Promise<Result<R>> {
        try {
            const result = await fetch(this.baseUrl + url, request);
            if (result.ok) {
                const data = await result.json();
                if (data.status === "success") {
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

    public static async postTrack(data: {track: string, description: string, title: string}) {
        const request: RequestInit = {
            method: "POST",
            body: JSON.stringify(data),
        };
        return this.fetch("/api/posts", request)
    }

}