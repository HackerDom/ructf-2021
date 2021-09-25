export class LocalStorage {
    private static readonly auth_name = "auth";

    static setAuth(auth: string): void {
        localStorage.setItem(this.auth_name, auth)
    }

    static getAuth(): string | null {
        return localStorage.getItem(this.auth_name);
    }
}
