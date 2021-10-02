import {JsonConverter, JsonCustomConvert} from "json2typescript";

@JsonConverter
export class FunctionConverter implements JsonCustomConvert<Function> {
    public serialize(data: Function): string {
        return data.toString();
    }

    public deserialize(data: string): Function {
        // eslint-disable-next-line no-new-func
        return new Function(data);
    }
}