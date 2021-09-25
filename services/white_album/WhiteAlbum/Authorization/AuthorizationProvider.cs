using System.Collections.Generic;
using System.Threading.Tasks;
using WhiteAlbum.Entities;
using WhiteAlbum.Entities.Users;
using WhiteAlbum.Stores;

namespace WhiteAlbum.Authorization
{
    public class AuthorizationProvider : IAuthorizationProvider
    {
        private readonly AlbumStore albumStore;
        private readonly SingleStore singleStore;

        public AuthorizationProvider(AlbumStore albumStore, SingleStore singleStore)
        {
            this.albumStore = albumStore;
            this.singleStore = singleStore;
        }

        public async Task<bool> HasSuperAdministratorAccess(UserId user)
        {
            return false;
        }

        public async Task<bool> HasAccessTo(UserId user, IEnumerable<Album> albums, IEnumerable<Single> singles, Permission permission)
        {
            var ownedAlbums = await albumStore.Get(user);
            var ownedSingles = await singleStore.Get(user);
            
            foreach (var album in albums)
            {
                if (!ownedAlbums.Contains(album))
                    return false;
            }
            
            foreach (var single in singles)
            {
                if (!ownedSingles.Contains(single))
                    return false;
            }

            return true;
        }
    }
}