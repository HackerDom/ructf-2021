using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Server.Kestrel.Core;
using Microsoft.Extensions.DependencyInjection;
using WhiteAlbum.Authorization;
using WhiteAlbum.Repository;
using WhiteAlbum.Stores;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Newtonsoft.Json;
using System.ComponentModel.DataAnnotations;
using WhiteAlbum.Helpers;

namespace WhiteAlbum
{
    public class Startup
    {
        public void ConfigureServices(IServiceCollection services)
        {
            // services.AddMvc().SetCompatibilityVersion(CompatibilityVersion.Version_3_0);
            
            services
                .AddControllers()
                .AddNewtonsoftJson(
                options =>
                {
                    foreach (var converter in JsonSerialization.Settings.Converters)
                        options.SerializerSettings.Converters.Add(converter);

                    options.SerializerSettings.NullValueHandling = NullValueHandling.Ignore;

                    options.SerializerSettings.Error += (_, args) =>
                    {
                        if (!args.ErrorContext.Handled)
                        {
                            var exception = args.ErrorContext.Error;
                            throw new ValidationException($"Bad request: {exception.GetType().Name}: {exception.Message}", exception);
                        }
                    };
                });

            services.Configure<KestrelServerOptions>(options => options.AllowSynchronousIO = true);
            services.DiscoverInternalControllers();

            services.AddSingleton<UserRepository>();
            services.AddSingleton<AlbumRepository>();
            services.AddSingleton<SingleRepository>();
            
            services.AddSingleton<AlbumStore>();
            services.AddSingleton<SingleStore>();
            services.AddSingleton<UserStore>();
            
            services.AddSingleton<IAuthorizationProvider, AuthorizationProvider>();
        }

        public void Configure(IApplicationBuilder application)
        {
            application.UsePathBase("/white_album");

            application.UseRouting();
            
            application.UseMiddleware<AuthenticationMiddleware>();

            application.UseEndpoints(endpoints => endpoints.MapControllers());
        }
    }
}