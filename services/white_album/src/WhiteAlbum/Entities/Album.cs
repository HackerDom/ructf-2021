using System;
using System.Collections.Immutable;
using WhiteAlbum.Entities.Users;

namespace WhiteAlbum.Entities
{
    public class Album
    {
        public AlbumId Id { get; }

        public AlbumName Name { get; init; }
        public AlbumMeta Meta { get; init; }
        public Date CreatedAt { get; }

        public ImmutableArray<SingleId> Singles { get; set; } = ImmutableArray<SingleId>.Empty;
        
        public UserId Owner { get; set; }

        public Album(AlbumId id, AlbumName name, AlbumMeta meta, Date createdAt)
        {
            Id = id;
            Name = name;
            Meta = meta;
            CreatedAt = createdAt;
        }

        #region Equality members

        public bool Equals(Album other)
        {
            return Id.Equals(other.Id) && Name.Equals(other.Name);
        }

        public override bool Equals(object? obj)
        {
            if (ReferenceEquals(null, obj)) return false;
            if (ReferenceEquals(this, obj)) return true;
            if (obj.GetType() != this.GetType()) return false;
            return Equals((Album)obj);
        }

        public override int GetHashCode()
        {
            return HashCode.Combine(Id, Name);
        }

        #endregion
    }
}