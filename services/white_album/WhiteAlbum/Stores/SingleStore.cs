using System;
using System.Collections.Concurrent;
using System.Collections.Immutable;
using System.Threading.Tasks;
using WhiteAlbum.Entities;
using WhiteAlbum.Entities.Users;
using WhiteAlbum.Requests;
using Single = WhiteAlbum.Entities.Single;

namespace WhiteAlbum.Stores
{
    public class SingleStore
    {
        private readonly ConcurrentDictionary<SingleId, Single> singles = new();
        private readonly ConcurrentDictionary<UserId, ImmutableArray<Single>> singlesByUser = new();
        

        public async Task<Single> Create(CreateSingleRequest request)
        {
            var single = new Single(request.Id, request.Name, request.Meta, request.Track, Context.User!.Id) ;
            var result = singles.GetOrAdd(request.Id, single);

            try
            {
                if (!ReferenceEquals(result, single))
                    throw new Exception("Single already exists.");
                
                return result;
            }
            finally
            {
                while (true)
                {
                    var usersAlbum= singlesByUser.GetOrAdd(result.Owner, _ => ImmutableArray<Single>.Empty);

                    if (usersAlbum.Contains(single))
                        break;
                    
                    if (singlesByUser.TryUpdate(result.Owner, usersAlbum.Add(single), usersAlbum))
                        break;
                }
            }
        }
        
        public async Task<Single> Get(SingleId singleId)
        {
            return singles[singleId];
        }
        
        
        public async Task<ImmutableArray<Single>> Get(UserId userId)
        {
            if (singlesByUser.TryGetValue(userId, out var result))
                return result;
            
            return ImmutableArray<Single>.Empty;
        }

    }
}