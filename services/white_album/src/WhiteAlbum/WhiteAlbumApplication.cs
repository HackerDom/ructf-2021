using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Extensions.DependencyInjection;
using Vostok.Applications.AspNetCore;
using Vostok.Applications.AspNetCore.Builders;
using Vostok.Configuration.Abstractions;
using Vostok.Configuration.Sources.Json;
using Vostok.Hosting.Abstractions;
using Vostok.Throttling.Config;
using WhiteAlbum.Entities;
using WhiteAlbum.Entities.Users;
using WhiteAlbum.Helpers;
using WhiteAlbum.Settings;
using WhiteAlbum.Stores;
using Single = WhiteAlbum.Entities.Single;

namespace WhiteAlbum
{
    public class WhiteAlbumApplication : VostokAspNetCoreApplication<Startup>
    {
        private UserStore userStore;
        private SingleStore singleStore;
        private AlbumStore albumStore;

        public static IConfigurationProvider ConfigurationProvider;

        public override void Setup(IVostokAspNetCoreApplicationBuilder builder, IVostokHostingEnvironment environment)
        {
            ConfigurationProvider = environment.ConfigurationProvider;
            ConfigurationProvider.SetupSourceFor<WhiteAlbumSettings>(new JsonFileSource(@$"{Environment.CurrentDirectory}/data/settings.json"));
            
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

            userStore = serviceProvider.GetService<UserStore>()!;
            if (File.Exists(settings.UsersDumpPath))
            {
                var users = Encoding.UTF8.GetString(File.ReadAllBytes(settings.UsersDumpPath)).FromJson<User[]>();
                userStore!.Initialize(users);
            }
            
            albumStore = serviceProvider.GetService<AlbumStore>()!;
            if (File.Exists(settings.AlbumsDumpPath))
            {
                var albums = Encoding.UTF8.GetString(File.ReadAllBytes(settings.AlbumsDumpPath)).FromJson<Album[]>();
                albumStore!.Initialize(albums);
            }
            
            singleStore = serviceProvider.GetService<SingleStore>()!;
            if (File.Exists(settings.SinglesDumpPath))
            {
                var singles = Encoding.UTF8.GetString(File.ReadAllBytes(settings.SinglesDumpPath)).FromJson<Single[]>();
                singleStore!.Initialize(singles);
            }
            
            singleStore.Start();
            albumStore.Start();
            userStore.Start();

            try
            {
                userStore.CreateInternal(User.SuperAdmin);
            }
            catch
            {
            }
            
            return base.WarmupAsync(environment, serviceProvider);
        }

        public override void DoDispose()
        {
            userStore.Stop();
            albumStore.Stop();
            singleStore.Stop();
            
            base.DoDispose();
        }
    }
}