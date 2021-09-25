using Vostok.Applications.AspNetCore;
using Vostok.Applications.AspNetCore.Builders;
using Vostok.Hosting.Abstractions;
using Vostok.Throttling.Config;

namespace WhiteAlbum
{
    internal class WhiteAlbumApplication : VostokAspNetCoreApplication<Startup>
    {
        public override void Setup(IVostokAspNetCoreApplicationBuilder builder, IVostokHostingEnvironment environment)
        {
            base.Setup(builder, environment);


            builder.SetupThrottling(
                throttling =>
                {
                    throttling.UseEssentials(() => new ThrottlingEssentials { });
                    throttling.DisableMetrics();
                });


            builder.SetupWebHost(
                webHost => webHost.ConfigureServices(
                    services =>
                    {
                     
                    }));
        }
    }
}