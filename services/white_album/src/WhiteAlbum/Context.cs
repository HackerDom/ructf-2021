using Vostok.Context;
using WhiteAlbum.Entities.Users;

namespace WhiteAlbum
{
    public class Context
    {
        public static User? User
        {
            get => FlowingContext.Globals.Get<User>();
            set => FlowingContext.Globals.Set(value);
        }
    }
}