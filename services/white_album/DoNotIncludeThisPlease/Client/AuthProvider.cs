using System;

namespace DoNotIncludeThisPlease.Client
{
    public class AuthProvider
    {
        private readonly Func<string?> apiKeyProvider;

        public AuthProvider(Func<string?> apiKeyProvider)
            => this.apiKeyProvider = apiKeyProvider;

        public AuthProvider(string? apiKey)
            : this(() => apiKey)
        {
        }

        public string? GetApiKey() => apiKeyProvider();
    }
}