using System;
using System.Threading.Tasks;
using Vostok.Clusterclient.Core;
using WhiteAlbum.Entities;
using WhiteAlbum.Requests;

namespace DoNotIncludeThisPlease.Client
{
    public class AlbumClient : RpcClientBase
    {
        public AlbumClient(string pathPrefix, IClusterClient client, IAuthProvider authProvider) : base(pathPrefix,
            client, authProvider)
        {
        }

        public Task<ClientResult> Create(CreateAlbumRequest request, TimeSpan timeout) =>
            Method("create").CallAsync(request, timeout);
            
            
        public Task<ClientResult<Album>> Get(GetAlbumRequest request, TimeSpan timeout) =>
            Method<Album>("get").CallAsync(request, timeout);
            
            
        public Task<ClientResult> Attach(AttachSingleToAlbumRequest request, TimeSpan timeout) =>
            Method("attach").CallAsync(request, timeout);
    }
}