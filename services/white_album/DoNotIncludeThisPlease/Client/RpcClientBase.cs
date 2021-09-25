using System;
using System.Threading;
using System.Threading.Tasks;
using DoNotIncludeThisPlease.Helpers;
using Vostok.Clusterclient.Core;
using Vostok.Clusterclient.Core.Model;

namespace DoNotIncludeThisPlease.Client
{
    public abstract class RpcClientBase : ClientBase
    {
        private readonly string path;

        protected RpcClientBase(string pathPrefix, IClusterClient client, IAuthProvider authProvider)
            : base(client, authProvider)
        {
            path = pathPrefix.TrimEnd('/');
        }

        protected static TResult CreateResult<TResult>(Response response)
        {
            if (response.Content == null)
                throw new InvalidOperationException("Empty response content");
            
            try
            {
                if (response.HasContent)
                    return response.Content.ToString().FromJson<TResult>();
                
                if (response.HasStream)
                    return response.Stream.FromJsonStream<TResult>();

                return string.Empty.FromJson<TResult>();
            }
            catch (Exception error)
            {
                throw new InvalidOperationException($"Can't deserialize an object of type '{typeof(TResult).Name}' from response content.", error);
            }
        }

        protected RemoteProcedureCall Method(string method)
        {
            return new RemoteProcedureCall($"{path}/{method}", this);
        }

        protected RemoteProcedureCall<TResult> Method<TResult>(string method)
        {
            return new RemoteProcedureCall<TResult>($"{path}/{method}", this);
        }

        private static Request CreateRequest(string methodPath, object? request)
        {
            var result = Request.Post(methodPath);

            if (request != null)
            {
                result = result.WithJsonContent(request);
            }

            return result;
        }

        private static bool IsSuccessful(ClusterResult result)
        {
            return result.Response.IsSuccessful;
        }

        private Task<HoustonContentResult> Download(string methodPath, object? request, TimeSpan timeout, CancellationToken cancellationToken)
        {
            return Download(CreateRequest(methodPath, request), IsSuccessful, timeout, cancellationToken);
        }

        private Task<HoustonResult<T>> SendRequest<T>(string methodPath, object? request, TimeSpan timeout, CancellationToken cancellationToken)
        {
            return SendRequest(CreateRequest(methodPath, request), CreateResult<T>, IsSuccessful, timeout, cancellationToken);
        }

        private Task<HoustonResult> SendRequest(string methodPath, object? request, TimeSpan? timeout, CancellationToken cancellationToken)
        {
            return SendRequest(CreateRequest(methodPath, request), IsSuccessful, timeout, cancellationToken);
        }

        protected class RemoteProcedureCall
        {
            private readonly string path;
            private readonly RpcClientBase client;

            public RemoteProcedureCall(string path, RpcClientBase client)
            {
                this.path = path;
                this.client = client;
            }

            public Task<HoustonResult> CallAsync<TRequest>(TRequest request, TimeSpan timeout, CancellationToken cancellationToken = default)
            {
                return client.SendRequest(path, request, timeout, cancellationToken);
            }

            public Task<HoustonResult> CallAsync(TimeSpan timeout, CancellationToken cancellationToken = default)
            {
                return client.SendRequest(path, null, timeout, cancellationToken);
            }

            public Task<HoustonContentResult> DownloadAsync<TRequest>(TRequest request, TimeSpan timeout, CancellationToken cancellationToken = default)
            {
                return client.Download(path, request, timeout, cancellationToken);
            }
        }

        protected class RemoteProcedureCall<TResult>
        {
            private readonly string path;
            private readonly RpcClientBase client;

            public RemoteProcedureCall(string path, RpcClientBase client)
            {
                this.path = path;
                this.client = client;
            }

            public Task<HoustonResult<TResult>> CallAsync<TRequest>(TRequest request, TimeSpan timeout, CancellationToken cancellationToken = default)
            {
                return client.SendRequest<TResult>(path, request, timeout, cancellationToken);
            }

            public Task<HoustonResult<TResult>> CallAsync(TimeSpan timeout, CancellationToken cancellationToken = default)
            {
                return client.SendRequest<TResult>(path, null, timeout, cancellationToken);
            }
        }
    }
}