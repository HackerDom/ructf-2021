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

        // Copy-pasted from full .NET framework
        public static unsafe int GetDeterministicHashCode(this string s)
        {
            fixed (char* chPtr = s)
            {
                var num1 = 352654597;
                var num2 = num1;
                var numPtr = (int*)chPtr;
                int length;
                for (length = s.Length; length > 2; length -= 4)
                {
                    num1 = ((num1 << 5) + num1 + (num1 >> 27)) ^ *numPtr;
                    num2 = ((num2 << 5) + num2 + (num2 >> 27)) ^ numPtr[1];
                    numPtr += 2;
                }

                if (length > 0)
                    num1 = ((num1 << 5) + num1 + (num1 >> 27)) ^ *numPtr;
                return num1 + num2 * 1566083941;
            }
        }

        public static byte[] ToByteArray(this string str) => Encoding.UTF8.GetBytes(str);
    }
}