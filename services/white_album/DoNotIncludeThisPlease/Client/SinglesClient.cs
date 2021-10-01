using System;
using System.Threading.Tasks;
using Vostok.Clusterclient.Core;
using WhiteAlbum.Requests;
using Single = WhiteAlbum.Entities.Single;

namespace DoNotIncludeThisPlease.Client
{
    public class SinglesClient : RpcClientBase
    {
        public SinglesClient(string pathPrefix, IClusterClient client, IAuthProvider authProvider) : base(pathPrefix, client, authProvider)
        {
        }

        public Task<ClientResult> Create(CreateSingleRequest request, TimeSpan timeout) =>
            Method("create").CallAsync(request, timeout);
            
            
        public Task<ClientResult<Single>> Get(GetSingleRequest request, TimeSpan timeout) =>
            Method<Single>("get").CallAsync(request, timeout);
            
            
        public Task<ContentResult> Mix(MixSingleRequest request, TimeSpan timeout) =>
            Method("mix").DownloadAsync(request, timeout);
    }
}