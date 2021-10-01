namespace WhiteAlbum.Entities.Users
{
    public record User(
        UserId Id,
        UserName Name,
        UserToken Token
      );
}