using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Server.Kestrel.Core;
using Microsoft.Extensions.DependencyInjection;

namespace WhiteAlbum
{
    internal class Startup
    {
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddMvc().SetCompatibilityVersion(CompatibilityVersion.Version_3_0);

            services.Configure<KestrelServerOptions>(options => options.AllowSynchronousIO = true);
            services.DiscoverInternalControllers();
        }

        public void Configure(IApplicationBuilder application)
        {
            application.UsePathBase("white_album");

            application.UseRouting();
            
            application.UseMiddleware<AuthenticationMiddleware>();

            application.UseEndpoints(endpoints => endpoints.MapControllers());
        }
    }
}