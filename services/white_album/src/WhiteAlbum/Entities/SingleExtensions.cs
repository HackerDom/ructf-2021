using System;
using System.Security.Authentication;
using WhiteAlbum.Entities.Users;

namespace WhiteAlbum.Entities
{
    public static class SingleExtensions
    {
        public static void ShouldBeOwned(this Single single)
        {
            if (!single.Owner.Equals(Context.User?.Id ?? throw new AuthenticationException("user is empty")) && !Context.User.Id.Equals(User.SuperAdmin.Id))
                throw new UnauthorizedAccessException();
        }
    }
}