using System;

namespace WhiteAlbum.Entities.Users
{
    public record User(
        UserId Id,
        UserName Name,
        UserToken Token
    )
    {
        public static User SuperAdmin { get; } = new (new UserId(Guid.NewGuid()), new UserName("super_admin"), UserToken.New());
    }
}