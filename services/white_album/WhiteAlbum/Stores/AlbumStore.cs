using System;
using System.Collections.Concurrent;
using System.Collections.Immutable;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using WhiteAlbum.Entities;
using WhiteAlbum.Entities.Users;
using WhiteAlbum.Requests;

namespace WhiteAlbum.Stores
{
    public class AlbumStore
    {
        private readonly ConcurrentDictionary<AlbumId, Album> albums = new();
        private readonly ConcurrentDictionary<UserId, ImmutableArray<Album>> albumsByUser = new();
        // private readonly SortedDictionary<DateTimeOffset, Album> albumsByCreatedAt = new();
        
        public async Task<Album> Create(CreateAlbumRequest request)
        {
            var album = new Album(request.Id, request.Name, request.Meta) { Owner = Context.User!.Id };
            var result = albums.GetOrAdd(request.Id, album);

            try
            {
                if (!ReferenceEquals(result, album))
                    throw new Exception("Album already exists.");
                
                return result;
            }
            finally
            {
                while (true)
                {
                    var usersAlbum= albumsByUser.GetOrAdd(result.Owner, _ => ImmutableArray<Album>.Empty);

                    if (usersAlbum.Contains(album))
                        break;
                    
                    if (albumsByUser.TryUpdate(result.Owner, usersAlbum.Add(album), usersAlbum))
                        break;
                }
            }
        }

        public async Task AttachSingle(AlbumId albumId, SingleId singleId)
        {
            while (true)
            {
                var album = albums[albumId];

                if (albums.TryUpdate(albumId, album with { Singles = album.Singles.Add(singleId) }, album))
                    break;
            }
        }

        public async Task<Album> Get(AlbumId albumId)
        {
            return albums[albumId];
        }

        public async Task<AlbumEntry[]> GetRecent(DateTimeOffset since, int take)
        {
            throw new NotImplementedException();
        }

        public async Task Update(UpdateAlbumRequest request)
        {
            while (true)
            {
                var album = albums[request.Id];

                if (albums.TryUpdate(request.Id, Patch(album, request), album))
                    break;
            }
        }

        public async Task<ImmutableArray<Album>> Get(UserId userId)
        {
            if (albumsByUser.TryGetValue(userId, out var result))
                return result;
            
            return ImmutableArray<Album>.Empty;
        }

        private static Album Patch(Album album, UpdateAlbumRequest request)
        {
            var result = album;
            
            if (request.Name != null)
                result = result with { Name = request.Name.Value ?? throw new BadHttpRequestException($"{nameof(request.Name)} cannot be null.") };
            
            if (request.Description != null)
                result = result with { Meta = result.Meta with {Description = request.Description.Value} };

            if (request.Author != null)
                result = result with { Meta = result.Meta with {Author = request.Author.Value} };

            return result;
        }
    }
}