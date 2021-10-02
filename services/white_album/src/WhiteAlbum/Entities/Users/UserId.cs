using System;

namespace WhiteAlbum.Entities.Users
{
    public class UserId
    {
        public Guid Id { get; }

        public UserId(Guid id)
        {
            Id = id;
        }

        protected bool Equals(UserId other)
        {
            return Id.Equals(other.Id);
        }

        public override bool Equals(object? obj)
        {
            if (ReferenceEquals(null, obj)) return false;
            if (ReferenceEquals(this, obj)) return true;
            if (obj.GetType() != this.GetType()) return false;
            return Equals((UserId)obj);
        }

        public override int GetHashCode()
        {
            return Id.GetHashCode();
        }
    }
}