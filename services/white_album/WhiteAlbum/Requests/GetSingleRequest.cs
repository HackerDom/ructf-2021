using WhiteAlbum.Entities;

namespace WhiteAlbum.Requests
{
    public class GetSingleRequest
    {
        public GetSingleRequest(SingleId id)
        {
            Id = id;
        }

        public SingleId Id { get; }
    }
}