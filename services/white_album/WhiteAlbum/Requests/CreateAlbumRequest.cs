using WhiteAlbum.Entities;
using WhiteAlbum.Entities.Users;

namespace WhiteAlbum.Requests
{
    public class CreateAlbumRequest
    {
        public CreateAlbumRequest(AlbumId id, AlbumName name, AlbumMeta meta)
        {
            Id = id;
            Name = name;
            Meta = meta;
        }

        public AlbumId Id { get; }

        public AlbumName Name { get; }
        public AlbumMeta Meta { get; }
    }
}