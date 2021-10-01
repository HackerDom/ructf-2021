using System;

namespace WhiteAlbum.Entities
{
    public record AlbumEntry(AlbumId Id, AlbumName Name, DateTimeOffset CreatedAt);
}