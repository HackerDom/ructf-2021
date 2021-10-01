using System;
using System.Threading.Tasks;
using WhiteAlbum.Entities.Users;

namespace WhiteAlbum.Users
{
    public interface IUserProvider
    {
        Task<User?> FindUserByApiToken(Guid apiTokenId);
    }
}