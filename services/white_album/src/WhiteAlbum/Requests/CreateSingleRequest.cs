using WhiteAlbum.Entities;
using WhiteAlbum.Tracks;

namespace WhiteAlbum.Requests
{
    public class CreateSingleRequest
    {
        public CreateSingleRequest(SingleId id, SingleMeta meta, SingleName name, Track track)
        {
            Id = id;
            Meta = meta;
            Track = track;
            Name = name;
        }

        public SingleId Id { get; }
        public SingleMeta Meta { get; }
        public Track Track { get; }
        public SingleName Name { get; }
    }
}