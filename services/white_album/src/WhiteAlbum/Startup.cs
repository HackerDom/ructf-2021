using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Server.Kestrel.Core;
using Microsoft.Extensions.DependencyInjection;
using WhiteAlbum.Authorization;
using WhiteAlbum.Repository;
using WhiteAlbum.Stores;
using Newtonsoft.Json;
using WhiteAlbum.Authentication;
using WhiteAlbum.Helpers;
using WhiteAlbum.Middleware;
using WhiteAlbum.Settings;
using AuthenticationMiddleware = WhiteAlbum.Middleware.AuthenticationMiddleware;

namespace WhiteAlbum
{
    public class Startup
    {
        public void ConfigureServices(IServiceCollection services)
        {
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
            
            services.AddSingleton<Authenticator>();
            services.AddSingleton<IAuthorizationProvider, AuthorizationProvider>();
        }

        public void Configure(IApplicationBuilder application)
        {
            application.UsePathBase(WhiteAlbumApplication.ConfigurationProvider.Get<WhiteAlbumSettings>().Prefix);

            application.UseRouting();
            
            application.UseMiddleware<AuthenticationMiddleware>();
            application.UseMiddleware<ExceptionHandleMiddleware>();

            application.UseEndpoints(endpoints => endpoints.MapControllers());
        }
    }
}