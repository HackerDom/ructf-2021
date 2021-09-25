using System;
using System.Threading;
using System.Threading.Tasks;
using DoNotIncludeThisPlease.Helpers;
using Vostok.Clusterclient.Core;
using Vostok.Clusterclient.Core.Model;

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

        protected async Task<HoustonResult<T>> SendRequest<T>(Request request, Func<Response, T> createResult, Func<ClusterResult, bool> isSuccessful, TimeSpan? timeout, CancellationToken cancellationToken = default)
        {
            request = AddAuthHeader(request);

            using var result = await client
                .SendAsync(request, timeout, cancellationToken: cancellationToken)
                .ConfigureAwait(false);

            return isSuccessful(result)
                ? new HoustonResult<T>(createResult(result.Response), true, result.Response.Code)
                : new HoustonResult<T>(default, false, result.Response.Code, GetErrorMessage(result.Response));
        }

        protected async Task<HoustonResult> SendRequest(Request request, Func<ClusterResult, bool> isSuccessful, TimeSpan? timeout, CancellationToken cancellationToken)
        {
            request = AddAuthHeader(request);

            var result = await client
                .SendAsync(request, timeout, cancellationToken: cancellationToken)
                .ConfigureAwait(false);

            return isSuccessful(result)
                ? new HoustonResult(true, result.Response.Code)
                : new HoustonResult(false, result.Response.Code, GetErrorMessage(result.Response));
        }

        protected async Task<HoustonContentResult> Download(Request request, Func<ClusterResult, bool> isSuccessful, TimeSpan? timeout, CancellationToken cancellationToken)
        {
            request = AddAuthHeader(request);

            var result = await client
                .SendAsync(request, timeout, cancellationToken: cancellationToken)
                .ConfigureAwait(false);

            return isSuccessful(result)
                ? new HoustonContentResult(result, true, result.Response.Code, null)
                : new HoustonContentResult(result, false, result.Response.Code, GetErrorMessage(result.Response));
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