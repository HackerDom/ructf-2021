using System;

namespace WhiteAlbum.Entities
{
    public class SingleId
    {
        public SingleId(Guid id)
        {
            Id = id;
        }

        public Guid Id { get; }

        public bool Equals(SingleId other)
        {
            return Id.Equals(other.Id);
        }

        public override bool Equals(object? obj)
        {
            if (ReferenceEquals(null, obj)) return false;
            if (ReferenceEquals(this, obj)) return true;
            if (obj.GetType() != this.GetType()) return false;
            return Equals((SingleId)obj);
        }

        public override int GetHashCode()
        {
            return Id.GetHashCode();
        }
    }
}