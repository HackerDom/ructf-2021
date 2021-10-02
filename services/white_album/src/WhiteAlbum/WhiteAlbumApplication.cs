using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Extensions.DependencyInjection;
using Vostok.Applications.AspNetCore;
using Vostok.Applications.AspNetCore.Builders;
using Vostok.Configuration.Sources.Json;
using Vostok.Hosting.Abstractions;
using Vostok.Throttling.Config;
using WhiteAlbum.Entities;
using WhiteAlbum.Entities.Users;
using WhiteAlbum.Helpers;
using WhiteAlbum.Settings;
using WhiteAlbum.Stores;

namespace WhiteAlbum
{
    public class WhiteAlbumApplication : VostokAspNetCoreApplication<Startup>
    {
        public override void Setup(IVostokAspNetCoreApplicationBuilder builder, IVostokHostingEnvironment environment)
        {
            environment.ConfigurationProvider.SetupSourceFor<WhiteAlbumSettings>(new JsonFileSource("white_album_settings"));
            
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
                        services.AddSingleton<Func<WhiteAlbumSettings>>(() => environment.ConfigurationProvider.Get<WhiteAlbumSettings>());
                    }));
        }

        public override Task WarmupAsync(IVostokHostingEnvironment environment, IServiceProvider serviceProvider)
        {
            var settings = serviceProvider.GetService<Func<WhiteAlbumSettings>>()!();

            if (File.Exists(settings.UsersLogPath))
            {
                var userStore = serviceProvider.GetService<UserStore>();
                var users = Encoding.UTF8.GetString(File.ReadAllBytes(settings.UsersLogPath)).FromJson<Dictionary<string, User>>();
                userStore!.Initialize(users);
            }
            
            if (File.Exists(settings.AlbumsLogPath))
            {
                var albumStore = serviceProvider.GetService<AlbumStore>();
                var albums = Encoding.UTF8.GetString(File.ReadAllBytes(settings.AlbumsLogPath)).FromJson<Dictionary<string, Album>>();
                albumStore!.Initialize(albums);
            }
            
            return base.WarmupAsync(environment, serviceProvider);
        }
    }
}