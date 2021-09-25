using WhiteAlbum.Entities.Users;
using WhiteAlbum.Tracks;

namespace WhiteAlbum.Entities
{
    public class Single
    {
        public Single(SingleId id, SingleName name, SingleMeta meta, Track track, UserId owner)
        {
            Id = id;
            Name = name;
            Meta = meta;
            Track = track;
            this.Owner = owner;
        }

        public SingleId Id { get; init; }
        public SingleName Name { get; init; }
        public SingleMeta Meta { get; init; }
        public Track Track { get; init; }
        public UserId Owner { get; }
    }
}