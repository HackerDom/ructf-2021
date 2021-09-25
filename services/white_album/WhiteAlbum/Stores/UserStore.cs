using System;
using System.Collections.Concurrent;
using System.Threading.Tasks;
using WhiteAlbum.Entities.Users;
using WhiteAlbum.Requests;

namespace WhiteAlbum.Stores
{
    public class UserStore
    {
        private readonly ConcurrentDictionary<UserId, User> users = new();
        private readonly ConcurrentDictionary<UserToken, User> usersByTokens = new();

        public async Task<User> Create(CreateUserRequest request)
        {
            users.TryGetValue(request.Id, out var user);
            user ??= new User(request.Id, request.Name, UserToken.New());

            try
            {
                if (!users.TryAdd(user.Id, user))
                    throw new Exception($"User with id: {user.Id} already exists.");
            }
            finally
            {
                usersByTokens[user.Token] = user;
            }
           
            return user;
        }

        public async Task<User> Get(UserToken userToken)
        {
            return usersByTokens[userToken];
        }
        
        public async Task<User> Get(UserId userId)
        {
            return users[userId];
        }
    }
}