using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using WhiteAlbum.Authentication;

namespace WhiteAlbum.Middleware
{
    public class AuthenticationMiddleware
    {
        private readonly Authenticator authenticator;
        private readonly RequestDelegate next;
        
        public const string ApiTokenCookieName = "Api-Token";


        public AuthenticationMiddleware(Authenticator authenticator, RequestDelegate next)
        {
            this.authenticator = authenticator;
            this.next = next;
        }

        public async Task Invoke(HttpContext context)
        {
            var apiTokenString = Extract(context.Request);

            Context.User = await authenticator.Authenticate(apiTokenString);

            await next(context);
        }
        
        private static string? Extract(HttpRequest request)
        {
            var apiTokenString = FindInAuthorizationHeader(request);
            if (!string.IsNullOrEmpty(apiTokenString))
            {
                return apiTokenString;
            }

            return request.Cookies.TryGetValue(ApiTokenCookieName, out apiTokenString)
                ? apiTokenString
                : null;
        }

        private static string? FindInAuthorizationHeader(HttpRequest request)
            => Extract(request);
    }
}