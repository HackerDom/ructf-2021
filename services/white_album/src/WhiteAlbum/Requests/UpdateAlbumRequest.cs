using WhiteAlbum.Entities;
using WhiteAlbum.Utility;

namespace WhiteAlbum.Requests
{
    public class UpdateAlbumRequest
    {
        public UpdateAlbumRequest(AlbumId id)
        {
            Id = id;
        }

        public AlbumId Id { get; }
        
        public Option<AlbumName>? Name { get; init; }
        public Option<string>? Author { get; init; }
        public Option<string>? Description { get; init; }
    }
}