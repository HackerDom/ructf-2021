using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Linq;
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
        private readonly ConcurrentDictionary<UserId, ImmutableArray<AlbumId>> albumsByUser = new();
        private readonly ConcurrentDictionary<Date, ConcurrentBag<AlbumId>> albumsByDate = new();

        public async Task<Album> Create(CreateAlbumRequest request)
        {
            var album = new Album(request.Id, request.Name, request.Meta) {
                Owner = Context.User?.Id ?? throw new UnauthorizedAccessException("User is empty.")
            };
            var result = albums.GetOrAdd(request.Id, album);

            var now = Date.Now();
            
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
                    var usersAlbum= albumsByUser.GetOrAdd(result.Owner, _ => ImmutableArray<AlbumId>.Empty);

                    if (usersAlbum.Contains(album.Id))
                        break;
                    
                    if (albumsByUser.TryUpdate(result.Owner, usersAlbum.Add(album.Id), usersAlbum))
                        break;
                }
                albumsByDate.GetOrAdd(now, _ => new()).Add(album.Id);
            }
        }

        public async Task AttachSingle(AlbumId albumId, SingleId singleId)
        {
            while (true)
            {
                var album = albums[albumId];

                if (albums.TryUpdate(albumId, new Album(album.Id, album.Name, album.Meta)
                {
                    Owner = album.Owner,
                    Singles = album.Singles.Add(singleId)
                }, album))
                    break;
            }
        }

        public async Task<Album> Get(AlbumId albumId)
        {
            return albums[albumId];
        }

        public async Task<AlbumEntry[]> GetByDate(Date date)
        {
            if (!albumsByDate.TryGetValue(date, out var albumIds))
                return Array.Empty<AlbumEntry>();
            
            return albumIds.Select(x => albums[x]).Select(x => new AlbumEntry(x.Id, x.Name, date)).ToArray();
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
            if (albumsByUser.TryGetValue(userId, out var ids))
            { 
                var result = new List<Album>(ids.Length);
                foreach (var albumId in ids)
                {
                    result.Add(albums[albumId]);
                }

                return result.ToImmutableArray();
            };
            
            return ImmutableArray<Album>.Empty;
        }

        private static Album Patch(Album album, UpdateAlbumRequest request)
        {
            var result = album;

            if (request.Name != null)
                result = new Album(album.Id, request.Name.Value ?? throw new Exception("Name cannot be null"), album.Meta)
                {
                    Owner = album.Owner,
                    Singles = album.Singles
                };
            
            if (request.Description != null)
                result = new Album(album.Id, album.Name, new AlbumMeta(album.Meta.Author, request.Description.Value))
                {
                    Owner = album.Owner,
                    Singles = album.Singles
                };

            if (request.Author != null)
                result = new Album(album.Id, album.Name, new AlbumMeta(request.Author.Value, album.Meta.Description))
                {
                    Owner = album.Owner,
                    Singles = album.Singles
                };

            return result;
        }
    }
}