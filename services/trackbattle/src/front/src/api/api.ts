export class api {
    private static readonly baseUrl: string = "";

    public static async fetch(url: string, request: RequestInit) {
        try {
            return fetch(this.baseUrl + url, request);
        } catch (e) {
            console.log(e);
        }
    }

    public static async postTrack(data: {track: string, description: string, title: string}) {
        const request: RequestInit = {
            method: "POST",
            body: JSON.stringify(data),
        };
        return this.fetch("/api/posts", request)
    }

}