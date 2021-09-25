using WhiteAlbum.Entities;

namespace WhiteAlbum.Requests
{
    public class GetAlbumRequest
    {
        public GetAlbumRequest(AlbumId id)
        {
            Id = id;
        }

        public AlbumId Id { get; }
    }
}