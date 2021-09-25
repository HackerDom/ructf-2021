using System;
using System.IO;
using Vostok.Clusterclient.Core.Model;

namespace DoNotIncludeThisPlease.Client
{
    public class HoustonContentResult : HoustonResult, IDisposable
    {
        private readonly ClusterResult result;
        private Stream? stream;
        private long? length;

        public HoustonContentResult(ClusterResult result, bool isSuccessful, ResponseCode responseCode, string? error)
            : base(isSuccessful, responseCode, error)
        {
            this.result = result;
        }

        public long Length
        {
            get
            {
                EnsureSuccess();

                if (!length.HasValue)
                {
                    if (result.Response.HasHeaders && long.TryParse(result.Response.Headers.ContentLength, out var parsedLength))
                        length = parsedLength;
                    else
                        throw new Exception("Can't parse content length");
                }

                return length.Value;
            }
        }

        public Stream Content
        {
            get
            {
                EnsureSuccess();

                if (stream != null)
                    return stream;

                if (result.Response.HasStream)
                    stream = result.Response.Stream;
                else if (result.Response.HasContent)
                    stream = result.Response.Content.ToMemoryStream();
                else
                    throw new Exception("Neither content nor stream was found in inner result");

                return stream;
            }
        }

        public string? GetFileName()
        {
            const string filenameConst = "filename=";

            var contentDisposition = result.Response.Headers["Content-Disposition"];
            if (string.IsNullOrEmpty(contentDisposition)
                || !contentDisposition.StartsWith(filenameConst)
                || contentDisposition.Length <= filenameConst.Length)
            {
                return null;
            }

            return contentDisposition[filenameConst.Length..].Trim('"');
        }

        public void Dispose()
        {
            result.Dispose();
        }
    }
}