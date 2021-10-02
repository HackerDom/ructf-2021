using System;
using System.Threading;
using System.Threading.Tasks;
using DoNotIncludeThisPlease.Helpers;
using Vostok.Clusterclient.Core;
using Vostok.Clusterclient.Core.Model;
using WhiteAlbum.Helpers;

namespace DoNotIncludeThisPlease.Client
{
    public abstract class ClientBase
    {
        private readonly IClusterClient client;
        private readonly IAuthProvider authProvider;

        protected ClientBase(IClusterClient client, IAuthProvider authProvider)
        {
            this.client = client;
            this.authProvider = authProvider;
        }

        protected async Task<ClientResult<T>> SendRequest<T>(Request request, Func<Response, T> createResult, Func<ClusterResult, bool> isSuccessful, TimeSpan? timeout, CancellationToken cancellationToken = default)
        {
            request = AddAuthHeader(request);

            using var result = await client
                .SendAsync(request, timeout, cancellationToken: cancellationToken)
                .ConfigureAwait(false);

            return isSuccessful(result)
                ? new ClientResult<T>(createResult(result.Response), true, result.Response.Code)
                : new ClientResult<T>(default, false, result.Response.Code, GetErrorMessage(result.Response));
        }

        protected async Task<ClientResult> SendRequest(Request request, Func<ClusterResult, bool> isSuccessful, TimeSpan? timeout, CancellationToken cancellationToken)
        {
            request = AddAuthHeader(request);

            var result = await client
                .SendAsync(request, timeout, cancellationToken: cancellationToken)
                .ConfigureAwait(false);

            return isSuccessful(result)
                ? new ClientResult(true, result.Response.Code)
                : new ClientResult(false, result.Response.Code, GetErrorMessage(result.Response));
        }

        protected async Task<ContentResult> Download(Request request, Func<ClusterResult, bool> isSuccessful, TimeSpan? timeout, CancellationToken cancellationToken)
        {
            request = AddAuthHeader(request);

            var result = await client
                .SendAsync(request, timeout, cancellationToken: cancellationToken)
                .ConfigureAwait(false);

            return isSuccessful(result)
                ? new ContentResult(result, true, result.Response.Code, null)
                : new ContentResult(result, false, result.Response.Code, GetErrorMessage(result.Response));
        }

        private Request AddAuthHeader(Request request)
            => request.WithHeader("Authorization", $"Api-key {authProvider.GetApiKey()}");

        private static string GetErrorMessage(Response response)
        {
            var content = response.Content.ToString();
            var msg = (content.TryFromJson<ErrorResult>(out var error) ? error?.Message : null).NullIfNotSignificant()
                      ?? content.NullIfNotSignificant()
                      ?? $"Error: {response.Code}";
            return msg;
        }
    }
}