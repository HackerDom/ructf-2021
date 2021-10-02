export function createObject<T>(o: object | null, properties: Partial<T>): T {
    const keyValuePairs = Object.entries(properties).map(([key, v]) => [key, {value: v}]);
    const propertiesDescriptors = Object.fromEntries(keyValuePairs);

    return Object.create(o, propertiesDescriptors);
}