using WhiteAlbum.Entities;

namespace WhiteAlbum.Requests
{
    public class MixSingleRequest
    {
        public MixSingleRequest(SingleId id)
        {
            Id = id;
        }

        public SingleId Id { get; }
    }
}