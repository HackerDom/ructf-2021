using Vostok.Context;

namespace DoNotIncludeThisPlease.Client
{
    public class ApiKey
    {
        public ApiKey(string? value)
        {
            Value = value;
        }

        public string? Value { get; set; }

        public static void Set(string? apikey)
        {
            FlowingContext.Globals.Set(new ApiKey(apikey));
        }

        public static string? Get()
        {
            return FlowingContext.Globals.Get<ApiKey>()?.Value;
        }
    }
}