using System;
using System.Linq;
using System.Threading.Tasks;
using WhiteAlbum.Entities;
using WhiteAlbum.Entities.Users;
using WhiteAlbum.Helpers;
using Single = WhiteAlbum.Entities.Single;

namespace WhiteAlbum.Authorization
{
    public class AuthorizationRequestBuilder : IAuthorizationRequestBuilder
    {
        private readonly IAuthorizationProvider authorizationProvider;
        private readonly User user;
        private readonly Single[] singles;
        private readonly Album[] albums;

        public AuthorizationRequestBuilder(
            IAuthorizationProvider authorizationProvider, 
            User user)
        {
            this.authorizationProvider = authorizationProvider;
            this.user = user;
            singles = Array.Empty<Single>();
            albums = Array.Empty<Album>();
        }

        private AuthorizationRequestBuilder(
            IAuthorizationProvider authorizationProvider,
            User user, 
            Single[] singles,
            Album[] albums)
        {
            this.authorizationProvider = authorizationProvider;
            this.user = user;
            this.singles = singles;
            this.albums = albums;
        }

        public async Task BySuperAdministratorAccess()
        {
            if (!await authorizationProvider.HasSuperAdministratorAccess(user.Id))
                throw new UnauthorizedAccessException($"Access is denied. User {user.Name} is not super admin.");
        }

        public Task<bool> HasSuperAdministratorAccess() =>
            authorizationProvider.HasSuperAdministratorAccess(user.Id);

       
        #region For

        public IAuthorizationRequestBuilder For(Single single) 
            => new AuthorizationRequestBuilder(authorizationProvider, this.user, this.singles.Concat(single).ToArray(), this.albums);

        public IAuthorizationRequestBuilder For(Album album)
            => new AuthorizationRequestBuilder(authorizationProvider, this.user, this.singles, this.albums.Concat(album).ToArray());
        
        public IAuthorizationRequestBuilder And(Single single) 
            => new AuthorizationRequestBuilder(authorizationProvider, this.user, this.singles.Concat(single).ToArray(), this.albums);

        public IAuthorizationRequestBuilder And(Album album)
            => new AuthorizationRequestBuilder(authorizationProvider, this.user, this.singles, this.albums.Concat(album).ToArray());

        #endregion
        


        #region Authorizer

        private async Task EnsureAccess(Permission requiredRole)
        {
            if (!await HasAccess(requiredRole))
                throw new UnauthorizedAccessException($"Access is denied. User {user.Name} do not have rights. Required role is {requiredRole}");
        }

        public async Task<bool> HasAccess(Permission permission)
        {
            if (await authorizationProvider.HasSuperAdministratorAccess(user.Id))
                return true;

            if (singles.Length > 0 || albums.Length > 0)
                return await authorizationProvider.HasAccessTo(user.Id, albums, singles, permission);
            
            return false;
        }


        public Task By(Permission role) => EnsureAccess(role);

        #endregion
    }
}