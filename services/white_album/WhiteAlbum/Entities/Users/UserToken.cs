using System;

namespace WhiteAlbum.Entities.Users
{
    public class UserToken
    {
        public Guid Id { get; }

        public UserToken(Guid id)
        {
            Id = id;
        }

        public static UserToken New() => new(Guid.NewGuid());

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