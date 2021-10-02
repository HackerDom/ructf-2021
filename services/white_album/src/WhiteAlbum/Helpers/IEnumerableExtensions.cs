﻿using System.Collections.Generic;

namespace WhiteAlbum.Helpers
{
    public static class IEnumerableExtensions
    {
        public static IEnumerable<T> Concat<T>(this IEnumerable<T> enumerable, T element)
        {
            foreach (var item in enumerable)
                yield return item;

            yield return element;
        }
    }
}