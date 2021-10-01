using WhiteAlbum.Entities;

namespace WhiteAlbum.Requests
{
    public class GetAllSinglesRequest
    {
        public GetAllSinglesRequest(AlbumId id)
        {
            Id = id;
        }

        public AlbumId Id { get; }
    }
}