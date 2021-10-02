using Vostok.Clusterclient.Core.Model;
using WhiteAlbum.Helpers;

namespace DoNotIncludeThisPlease.Helpers
{
    public static class RequestExtensions
    {
        public static Request WithJsonContent(this Request request, object body)
        {
            return request
                .WithContentTypeHeader("application/json")
                .WithContent(body.ToJson());
        }
    }
}