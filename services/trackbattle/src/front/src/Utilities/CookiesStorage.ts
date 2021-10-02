import Cookies from 'universal-cookie';

export class CookiesStorage {
    private static cookies = new Cookies();

    static setAuth(auth: string): void {
        this.cookies.set('XTBAuth', auth)
    }

    static removeAuth(): void {
        this.cookies.remove('XTBAuth')
    }

    static getAuth(): string | null {
        return this.cookies.get('XTBAuth')
    }
}
