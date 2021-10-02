using System;
using System.Security.Authentication;
using System.Threading.Tasks;
using WhiteAlbum.Entities.Users;
using WhiteAlbum.Repository;
using WhiteAlbum.Settings;
using WhiteAlbum.Users;

namespace WhiteAlbum.Authentication
{
    public class Authenticator
    {
        private readonly UserRepository userRepository;
        private readonly Func<WhiteAlbumSettings> getSettings;

        public Authenticator(UserRepository userRepository, Func<WhiteAlbumSettings> getSettings)
        {
            this.userRepository = userRepository;
            this.getSettings = getSettings;
        }

        public async Task<User?> Authenticate(string? apiTokenString)
        {
            if (apiTokenString == null)
                return null;

            if (apiTokenString == getSettings().SuperAdminApiKey)
                return User.SuperAdmin;
            
            if (!Guid.TryParse(apiTokenString, out var apiTokenId))
                throw new AuthenticationException("A valid API token was not specified with the request.");

            var user = await userRepository.Get(new (apiTokenId));
            if (user == null)
                throw new AuthenticationException("User for provided API token was not found.");

            return user;
        }
    }
}