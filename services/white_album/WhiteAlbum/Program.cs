﻿using Vostok.Hosting;
using Vostok.Hosting.Setup;

namespace WhiteAlbum
{
    class 
        Program
    {
        static void Main(string[] args)
        {
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