using System.Collections.Generic;
using System.Threading.Tasks;
using WhiteAlbum.Entities;
using WhiteAlbum.Entities.Users;

namespace WhiteAlbum.Authorization
{
    public interface IAuthorizationProvider
    {
        Task<bool> HasSuperAdministratorAccess(UserId user);
        Task<bool> HasAccessTo(UserId user, IEnumerable<Album> albums, IEnumerable<Single> singles, Permission permission);
    }
}