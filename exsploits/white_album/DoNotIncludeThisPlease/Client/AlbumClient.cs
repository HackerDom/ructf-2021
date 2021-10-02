using System;
using System.Threading.Tasks;
using Vostok.Clusterclient.Core;
using WhiteAlbum.Entities;
using WhiteAlbum.Requests;
using Single = WhiteAlbum.Entities.Single;

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
        
        public Task<ClientResult<AlbumEntry[]>> GetByDate(GetByDateRequest request, TimeSpan timeout) =>
            Method<AlbumEntry[]>("get_by_date").CallAsync(request, timeout);
            
            
        public Task<ClientResult> Attach(AttachSingleToAlbumRequest request, TimeSpan timeout) =>
            Method("attach").CallAsync(request, timeout);

        public Task<ClientResult<Single[]>> GetAllSingles(GetAllSinglesRequest request, TimeSpan timeout) =>
            Method<Single[]>("get_all_singles").CallAsync(request, timeout);
    }
}