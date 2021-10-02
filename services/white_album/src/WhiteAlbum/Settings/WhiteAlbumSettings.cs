
using Vostok.Configuration.Abstractions.Attributes;

namespace WhiteAlbum.Settings
{
    public class WhiteAlbumSettings
    {
        [Optional] 
        public string UsersDumpPath = "users_dump";
        [Optional] 
        public string AlbumsDumpPath = "albums_dump";

        [Optional]
        public string SinglesDumpPath = "singles_dump";
    }
}