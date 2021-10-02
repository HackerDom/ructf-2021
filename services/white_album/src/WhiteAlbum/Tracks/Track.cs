using System;

namespace WhiteAlbum.Tracks
{
    public class Track
    {
        public Track(string[] tokens)
        {
            Tokens = tokens;
        }

        public string[] Tokens { get; init; }
    }
}