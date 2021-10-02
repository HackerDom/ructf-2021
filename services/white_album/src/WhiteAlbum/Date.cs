using System;

namespace WhiteAlbum
{
    public record Date(int Year, int Month, int Day, int Hour, int Minute)
    {
        public static Date Now()
        {
            var now = DateTime.UtcNow;
            return new Date(now.Year, now.Month, now.Day, now.Hour, now.Minute);
        }
    }
}