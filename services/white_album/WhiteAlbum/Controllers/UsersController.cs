using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using WhiteAlbum.Authorization;
using WhiteAlbum.Entities.Users;
using WhiteAlbum.Repository;
using WhiteAlbum.Requests;

namespace WhiteAlbum.Controllers
{
    public class UsersController : BaseController
    {
        private readonly UserRepository userRepository;


        public UsersController(UserRepository userRepository, IAuthorizationProvider authorizationProvider) : base(authorizationProvider)
        {
            this.userRepository = userRepository;
        }

        [HttpPost("user/create")]
        public async Task<UserToken> Create([FromBody] CreateUserRequest request)
        {
            var user = await userRepository.Create(request);

            return user.Token;
        }
    }
}