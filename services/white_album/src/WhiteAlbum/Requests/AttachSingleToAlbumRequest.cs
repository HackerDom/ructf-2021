using WhiteAlbum.Entities;

namespace WhiteAlbum.Requests
{
    public class AttachSingleToAlbumRequest
    {
        public AttachSingleToAlbumRequest(SingleId single, AlbumId albumId)
        {
            Single = single;
            AlbumId = albumId;
        }

        public SingleId Single { get; }
        
        public AlbumId AlbumId { get; }
    }
}