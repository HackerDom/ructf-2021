using System.Threading.Tasks;
using Microsoft.AspNetCore.Identity;
using WhiteAlbum.Entities.Users;
using WhiteAlbum.Requests;
using WhiteAlbum.Stores;

namespace WhiteAlbum.Repository
{
    public class UserRepository
    {
        private readonly UserStore userStore;

        public UserRepository(UserStore userStore)
        {
            this.userStore = userStore;
        }

        public async Task<User> Create(CreateUserRequest request)
        {
            return await userStore.Create(request);
        }

        public async Task<User> Get(UserToken userToken)
        {
            return await userStore.Get(userToken);
        }
    }
}