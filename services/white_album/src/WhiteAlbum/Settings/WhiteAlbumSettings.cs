
using Vostok.Configuration.Abstractions.Attributes;

namespace WhiteAlbum.Settings
{
    public class WhiteAlbumSettings
    {
        [Optional] 
        public string UsersLogPath = "users_dump";
        [Optional] 
        public string AlbumsLogPath = "albums_dump";

        [Optional]
        public string SinglesLogPath = "singles_dump";
    }
}