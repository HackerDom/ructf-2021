using System;
using System.Collections.Concurrent;
using System.Linq;
using System.Reflection;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace WhiteAlbum.Helpers
{
    public class StringSerializationJsonConverter : JsonConverter
    {
        private readonly ConcurrentDictionary<Type, bool> canConvertCache = new ConcurrentDictionary<Type, bool>();
        private readonly ConcurrentDictionary<Type, Func<object, string>?> asStringCache = new ConcurrentDictionary<Type, Func<object, string>?>();
        private readonly ConcurrentDictionary<Type, Func<string, object?>> factoryCache = new ConcurrentDictionary<Type, Func<string, object?>>();

        public override void WriteJson(JsonWriter writer, object? value, JsonSerializer serializer)
        {
            if (value == null)
            {
                JValue.CreateNull().WriteTo(writer);
                return;
            }

            var asString = asStringCache.GetOrAdd(value.GetType(), GetAsString) ?? (obj => obj.ToString()!);
            writer.WriteValue(asString(value));
        }

        public override object? ReadJson(JsonReader reader, Type objectType, object? existingValue, JsonSerializer serializer)
        {
            if (reader.TokenType == JsonToken.Null)
                return null;

            return factoryCache.GetOrAdd(objectType, GetFactory)(JToken.Load(reader).Value<string>());
        }

        public override bool CanConvert(Type objectType)
        {
            return canConvertCache.GetOrAdd(objectType, _ => objectType.GetCustomAttributes(typeof(StringSerializationAttribute), true).Any());
        }

        private static Func<object, string>? GetAsString(Type type)
        {
            var method = type
                .GetMethods(BindingFlags.Public | BindingFlags.Instance)
                .FirstOrDefault(m => !m.GetParameters().Any() && m.ReturnType == typeof(string));

            return method != null ? obj => (string)method.Invoke(obj, Array.Empty<object>())! : default(Func<object, string>);
        }

        private static Func<string, object?> GetFactory(Type type)
        {
            if (type.IsAbstract)
                throw new InvalidOperationException($"Expected non-abstract class, but found {type.Name}");

            var parser = type
                .GetMethods(BindingFlags.Public | BindingFlags.Static)
                .FirstOrDefault(m => m.GetParameters().Length == 1 && m.GetParameters()[0].ParameterType == typeof(string) && m.ReturnType == type);

            if (parser != null)
                return str => parser.Invoke(null, new object[] {str});

            var constructor = type.GetConstructors(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.CreateInstance | BindingFlags.Instance)
                .Where(c => c.GetParameters().Length == 1 && c.GetParameters()[0].ParameterType == typeof(string))
                .OrderBy(c => c.GetCustomAttribute<JsonConstructorAttribute>() != null ? 0 : 1)
                .FirstOrDefault(c => c.GetCustomAttribute<JsonConstructorAttribute>() != null || c.IsPublic);
            
            if (constructor == null)
                throw new InvalidOperationException($"Constructor 'public {type.Name}(string)' or parser 'public static {type.Name}(string)' or constructor with [JsonConstructor] attribute not found");

            return str => constructor.Invoke(new object[] {str});
        }
    }
}