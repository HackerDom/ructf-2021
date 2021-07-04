import {JsonConvert} from "json2typescript";

export class JsonSerializer {
    private static readonly jsonConvert = new JsonConvert();

    public static serialize<T>(data: T): any {
        return JsonSerializer.jsonConvert.serialize(data);
    }

    public static deserialize<T>(json: any, type: {new (): T;}): T | null {
        if (json === null) {
            return null;
        }

        return JsonSerializer.jsonConvert.deserializeObject(json, type)
    }
}