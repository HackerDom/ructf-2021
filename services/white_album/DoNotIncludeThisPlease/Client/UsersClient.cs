using System;
using System.Threading.Tasks;
using Vostok.Clusterclient.Core;
using WhiteAlbum.Entities.Users;
using WhiteAlbum.Requests;

namespace DoNotIncludeThisPlease.Client
{
    public class UsersClient : RpcClientBase
    {
        public UsersClient(string pathPrefix, IClusterClient client, IAuthProvider authProvider) : base(pathPrefix, client, authProvider)
        {
        }
        
        public Task<ClientResult<UserToken>> Create(CreateUserRequest request, TimeSpan timeout) =>
            Method<UserToken>("create").CallAsync(request, timeout);
    }
}