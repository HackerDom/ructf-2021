using System;
using Vostok.Hosting;

namespace WhiteAlbum
{
    class Program
    {
        static void Main(string[] args)
        {
            var host = new VostokHost(new VostokHostSettings(new WhiteAlbumApplication(), builder => {  }));

            host.WithConsoleCancellation().RunAsync().GetAwaiter().GetResult();
        }
    }
}