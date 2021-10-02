using System;
using System.Security.Authentication;

namespace WhiteAlbum.Entities
{
    public static class SingleExtensions
    {
        public static void ShouldBeOwned(this Single single)
        {
            if (!single.Owner.Equals(Context.User?.Id ?? throw new AuthenticationException("user is empty")))
                throw new UnauthorizedAccessException();
        }
    }
}