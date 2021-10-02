using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Vostok.Commons.Time;
using Vostok.Logging.Abstractions;
using WhiteAlbum.Entities.Users;
using WhiteAlbum.Helpers;
using WhiteAlbum.Requests;
using WhiteAlbum.Settings;

namespace WhiteAlbum.Stores
{
    public class UserStore
    {
        private readonly ConcurrentDictionary<UserId, User> users = new();
        private readonly ConcurrentDictionary<UserToken, User> usersByTokens = new();
        
        private readonly Func<WhiteAlbumSettings> getSettings;
        private readonly PeriodicalAction action;

        public UserStore(Func<WhiteAlbumSettings> getSettings, ILog log)
        {
            this.getSettings = getSettings;

            action = new PeriodicalAction(() => Dump(), e => log.Error(e), () => 1.Seconds());
        }

        public void Start()
        {
            action.Start();
        }
        
        public void Stop()
        {
            action.Stop();
        }

        public void Initialize(IEnumerable<User>? users)
        {
            if (users == null)
                return;
            
            foreach (var user in users)
            {
                CreateInternal(user);
            }
        }

        public void Dump()
        {
            if (!File.Exists(getSettings().UsersDumpPath))
                File.Create(getSettings().UsersDumpPath).Dispose();

            var content = users.Select(x => x.Value).ToJson();
            
            if (content.Length < 3)
                return;
            
            var tmpFileName = $"{getSettings().UsersDumpPath}_tmp_{Guid.NewGuid()}";
            using (var tmpFile = new FileStream(tmpFileName, FileMode.Create))
            {
                tmpFile.Write(Encoding.UTF8.GetBytes(content));
            }
            
            File.Replace(tmpFileName, getSettings().UsersDumpPath, null);
        }

        public async Task<User> Create(CreateUserRequest request)
        {
            users.TryGetValue(request.Id, out var user);
            user ??= new User(request.Id, request.Name, UserToken.New());

            return CreateInternal(user);
        }

        private User CreateInternal(User user)
        {
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