using System;
using Vostok.Clusterclient.Core;
using Vostok.Clusterclient.Transport;
using Vostok.Logging.Abstractions;

namespace DoNotIncludeThisPlease.Client
{
    public class Client
    {
      

        public Client(string url, IAuthProvider authProvider, ILog log)
        {
            var client = new ClusterClient(
                log.ForContext<Client>(),
                config =>
                {
                    config.SetupUniversalTransport(
                        new UniversalTransportSettings
                        {
                            UseResponseStreaming = size => size >= 1 * 1024 * 1024
                        });


                    config.Logging.LogReplicaRequests = false;
                    config.Logging.LogResultDetails = false;
                    
                    config.SetupExternalUrl(new Uri(url));
                });

            AlbumClient = new AlbumClient("album", client, authProvider);
            SinglesClient = new SinglesClient("single", client, authProvider);
            UsersClient = new UsersClient("user", client, authProvider);
        }

        public AlbumClient AlbumClient { get; }

        public SinglesClient SinglesClient { get; }
        
        public UsersClient UsersClient { get; }
    }
}