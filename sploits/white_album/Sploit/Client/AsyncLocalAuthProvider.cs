namespace DoNotIncludeThisPlease.Client
{
    public class AsyncLocalAuthProvider : IAuthProvider
    {
        public string? GetApiKey()
        {
            return ApiKey.Get();
        }
    }
}