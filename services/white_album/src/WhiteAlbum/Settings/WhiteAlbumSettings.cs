
using Vostok.Configuration.Abstractions.Attributes;

namespace WhiteAlbum.Settings
{
    public class WhiteAlbumSettings
    {
        [Optional] 
        public string UsersDumpPath = "data/users_dump";
        [Optional] 
        public string AlbumsDumpPath = "data/albums_dump";

        [Optional]
        public string SinglesDumpPath = "data/singles_dump";
    }
}