using System;

namespace WhiteAlbum.Requests
{
    public class GetRecentlyCreatedRequest
    {
        public DateTimeOffset StartDate { get; }
        public int Count { get; }
    }
}