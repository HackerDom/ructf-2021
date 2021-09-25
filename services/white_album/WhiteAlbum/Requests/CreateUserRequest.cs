using WhiteAlbum.Entities.Users;

namespace WhiteAlbum.Requests
{
    public class CreateUserRequest
    {
        public CreateUserRequest(UserId id, UserName name)
        {
            Id = id;
            Name = name;
        }

        public UserId Id { get; }
        public UserName Name { get; }
    }
}