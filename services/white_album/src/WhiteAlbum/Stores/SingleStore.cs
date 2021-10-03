using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Vostok.Commons.Time;
using Vostok.Logging.Abstractions;
using WhiteAlbum.Entities;
using WhiteAlbum.Entities.Users;
using WhiteAlbum.Helpers;
using WhiteAlbum.Requests;
using WhiteAlbum.Settings;
using Single = WhiteAlbum.Entities.Single;

namespace WhiteAlbum.Stores
{
    public class SingleStore
    {
        private readonly ConcurrentDictionary<SingleId, Single> singles = new();
        private readonly ConcurrentDictionary<UserId, ImmutableArray<Single>> singlesByUser = new();
        private readonly ConcurrentDictionary<Date, ConcurrentBag<SingleId>> singlesByDate = new();

        private readonly Func<WhiteAlbumSettings> getSettings;
        private readonly PeriodicalAction action;

        public SingleStore(Func<WhiteAlbumSettings> getSettings, ILog log)
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
        
        public void Dump()
        {
            if (!File.Exists(getSettings().SinglesDumpPath))
                File.Create(getSettings().SinglesDumpPath).Dispose();
            
            var content = singles.Select(x => x.Value).ToJson();
            
            if (content.Length < 3)
                return;
            
            var tmpFileName = $"{getSettings().SinglesDumpPath}_tmp_{Guid.NewGuid()}";
            using (var tmpFile = new FileStream(tmpFileName, FileMode.Create))
            {
                tmpFile.Write(Encoding.UTF8.GetBytes(content));
            }
            
            File.Replace(tmpFileName, getSettings().SinglesDumpPath, null);
        }

        public void Initialize(IEnumerable<Single>? signles)
        {
            if (signles == null)
                return;
            
            foreach (var  single in signles)
            {
                CreateInternal(single);
            }
        }
        
        public async Task<Single> Create(CreateSingleRequest request)
        {
            var now = Date.Now();

            var single = new Single(request.Id, request.Name, request.Meta, request.Track, Context.User?.Id ?? throw new Exception("User is empty"), now) ;

            return CreateInternal(single);
        }
        
        private Single CreateInternal(Single single)
        {
            var result = singles.GetOrAdd(single.Id, single);

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
                
                singlesByDate.GetOrAdd(single.CreatedAt, _ => new()).Add(single.Id);
            }
        }
        
        public async Task<Single> Get(SingleId singleId)
        {
            return singles[singleId];
        }
        
        public async Task<SingleEntry[]> GetByDate(Date date)
        {
            if (!singlesByDate.TryGetValue(date, out var singleIds))
                return Array.Empty<SingleEntry>();
            return singleIds.Select(x => singles[x]).Select(x => new SingleEntry(x.Id, x.Name, date)).ToArray();
        }
        
        public async Task<ImmutableArray<Single>> Get(UserId userId)
        {
            if (singlesByUser.TryGetValue(userId, out var result))
                return result;
            
            return ImmutableArray<Single>.Empty;
        }
    }
}