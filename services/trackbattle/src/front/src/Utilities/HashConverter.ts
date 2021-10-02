import {SHA256} from 'crypto-ts';

export async function sha256(message: string): Promise<string> {
    return SHA256(message);
}

export function toBase64(message: string): string {
    return btoa(message);
}

export function fromBase64(message: string): string {
    return atob(message);
}