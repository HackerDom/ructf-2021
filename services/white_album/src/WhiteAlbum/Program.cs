using System;
using System.IO;
using System.Text;
using Newtonsoft.Json;
using Vostok.Hosting;
using Vostok.Hosting.Setup;
using WhiteAlbum.Entities;
using WhiteAlbum.Entities.Users;
using WhiteAlbum.Requests;
using WhiteAlbum.Tracks;

namespace WhiteAlbum
{
    class Program
    {
        static void Main(string[] args)
        {
            if (!File.Exists(@$"{Environment.CurrentDirectory}/data/settings.json"))
            {
                File.WriteAllBytes(@$"{Environment.CurrentDirectory}/data/settings.json", Encoding.UTF8.GetBytes(
                    $"{{\"Prefix\": \"/white_album\",\"SuperAdminApKey\": \"{Guid.NewGuid()}\",\"UsersDumpPath\": \"data/users_dump\",\"AlbumsDumpPath\": \"data/albums_dump\",\"SinglesDumpPath\": \"data/singles_dump\"}}"));
            }
            
            void EnvironmentSetup(IVostokHostingEnvironmentBuilder builder)
            {
                builder
                    .SetupApplicationIdentity(
                        identityBuilder => identityBuilder
                            .SetEnvironment("environment")
                            .SetProject("White")
                            .SetApplication("Album")
                            .SetInstance("0"))
                    .SetupLog(logBuilder => logBuilder.SetupFileLog())
                    .SetPort(1234);
            }
            
            var host = new VostokHost(new VostokHostSettings(new WhiteAlbumApplication(), EnvironmentSetup));

            host.WithConsoleCancellation().RunAsync().GetAwaiter().GetResult();
        }
    }
}