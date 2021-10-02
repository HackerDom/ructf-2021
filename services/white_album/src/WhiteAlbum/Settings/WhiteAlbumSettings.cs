
using Vostok.Configuration.Abstractions.Attributes;

namespace WhiteAlbum.Settings
{
    public class WhiteAlbumSettings
    {
        [Required] 
        public string Prefix = "/prefix";

        public string SuperAdminApiKey = "with_this_api_key_you_have_access_to_everything";
        
        public string UsersDumpPath = "data/users_dump";
        
        public string AlbumsDumpPath = "data/albums_dump";

        public string SinglesDumpPath = "data/singles_dump";
    }
}