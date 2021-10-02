using System;
using System.Text;

namespace DoNotIncludeThisPlease.Helpers
{
    public static class StringExtensions
    {
        public static byte[] ToUtf8Bytes(this string @string) => Encoding.UTF8.GetBytes(@string);

        public static string ToUtf8String(this byte[] bytes) => Encoding.UTF8.GetString(bytes);

        public static bool IsSignificant(this string? str) => !string.IsNullOrWhiteSpace(str);

        public static string? NullIfNotSignificant(this string? str) => str.IsSignificant() ? str : null;

        public static string? WithPrefix(this string? str, string prefix) => str.IsSignificant() ? $"{prefix}{str}" : str;

        public static string? WithSuffix(this string? str, string suffix) => str.IsSignificant() ? $"{str}{suffix}" : str;

        public static string? WithUpperFirstLetter(this string str) => str.Length == 0 ? str : $"{char.ToUpperInvariant(str[0])}{str.Substring(1)}";

        public static string? WithLowerFirstLetter(this string str) => str.Length == 0 ? str : $"{char.ToLowerInvariant(str[0])}{str.Substring(1)}";

        public static string TrimEnd(this string input, string? suffixToRemove, StringComparison comparisonType = StringComparison.CurrentCulture)
        {
            if (suffixToRemove != null && input.EndsWith(suffixToRemove, comparisonType))
            {
                return input.Substring(0, input.Length - suffixToRemove.Length);
            }

            return input;
        }

        public static StringBuilder AppendIf(this StringBuilder builder, string value, bool conditionResult) =>
            conditionResult ? builder.Append(value) : builder;

     

        public static byte[] ToByteArray(this string str) => Encoding.UTF8.GetBytes(str);
    }
}