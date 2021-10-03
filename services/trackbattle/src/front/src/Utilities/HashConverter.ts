import {sha256_js} from "./sha256_js";

export function sha256(message: string): string {
    return String(sha256_js(message));
}

export function toBase64(message: string): string {
    return btoa(message);
}

export function fromBase64(message: string): string {
    return atob(message);
}