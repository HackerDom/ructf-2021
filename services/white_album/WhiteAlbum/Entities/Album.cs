using System.Collections.Immutable;
using System.Text.Json.Serialization;
using WhiteAlbum.Entities.Users;

namespace WhiteAlbum.Entities
{
    public class Album
    {
        // [JsonIgnore]

        public AlbumId Id { get; }

        // [JsonIgnore]

        public AlbumName Name { get; init; }
        // [JsonIgnore]

        public AlbumMeta Meta { get; init; }
       
        // [JsonIgnore]

        public ImmutableArray<SingleId> Singles { get; set; } = ImmutableArray<SingleId>.Empty;
        
        // [JsonIgnore]

        public UserId Owner { get; set; }

        [JsonIgnore]
        public string Signature => $"{Id}/{Name}";

        public Album(AlbumId id, AlbumName name, AlbumMeta meta)
        {
            Id = id;
            Name = name;
            Meta = meta;
        }

        #region Equality members

        public override bool Equals(object? obj)
        {
            if (ReferenceEquals(null, obj)) return false;
            if (ReferenceEquals(this, obj)) return true;
            if (obj.GetType() != this.GetType()) return false;
            return Equals((Album)obj);
        }
        
        public bool Equals(Album other)
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