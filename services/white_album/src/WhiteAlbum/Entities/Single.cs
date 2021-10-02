using WhiteAlbum.Entities.Users;
using WhiteAlbum.Tracks;

namespace WhiteAlbum.Entities
{
    public class Single
    {
        public Single(SingleId id, SingleName name, SingleMeta meta, Track track, UserId owner, Date createdAt)
        {
            Id = id;
            Name = name;
            Meta = meta;
            Track = track;
            this.Owner = owner;
            CreatedAt = createdAt;
        }

        public SingleId Id { get; init; }
        public SingleName Name { get; init; }
        
        public string Signature => $"{Id}/{Name}";
        public SingleMeta Meta { get; init; }
        public Track Track { get; init; }
        public UserId Owner { get; }
        public Date CreatedAt { get; }


        #region Equality members

        public override bool Equals(object? obj)
        {
            if (ReferenceEquals(null, obj)) return false;
            if (ReferenceEquals(this, obj)) return true;
            if (obj.GetType() != this.GetType()) return false;
            return Equals((Single)obj);
        }
        
        public bool Equals(Single other)
        {
            return Signature.Equals(other.Signature);
        }

        public override int GetHashCode()
        {
            return Signature.GetHashCode();
        }

        #endregion
    }
}