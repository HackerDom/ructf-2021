using System;
using System.Security.Authentication;
using System.Threading.Tasks;
using WhiteAlbum.Entities.Users;
using WhiteAlbum.Repository;
using WhiteAlbum.Users;

namespace WhiteAlbum.Authentication
{
    public class Authenticator
    {
        private readonly UserRepository userRepository;

        public Authenticator(UserRepository userRepository)
        {
            this.userRepository = userRepository;
        }

        public async Task<User> Authenticate(string? apiTokenString)
        {
            if (!Guid.TryParse(apiTokenString, out var apiTokenId))
                throw new AuthenticationException("A valid API token was not specified with the request.");

            var user = await userRepository.Get(new (apiTokenId));
            if (user == null)
                throw new AuthenticationException("User for provided API token was not found.");

            return user;
        }
    }
}