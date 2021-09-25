using System;

public class CaseToleranceStringKey : IEquatable<CaseToleranceStringKey>, IComparable<CaseToleranceStringKey>
{
    private static readonly StringComparer Comparer = StringComparer.OrdinalIgnoreCase;

    private readonly string value;

    public CaseToleranceStringKey(string value)
    {
        if (value == null)
            throw new ArgumentNullException(nameof(value), "Expected not null string");

        this.value = string.IsNullOrWhiteSpace(value)
            ? throw new ArgumentException("Expected significant string", nameof(value))
            : value;
    }

    public override string ToString() => value;

    #region Equality memebers

    public bool Equals(CaseToleranceStringKey? other) => other?.GetType() == GetType() && Comparer.Equals(other.value, value);

    public int CompareTo(CaseToleranceStringKey other) => Comparer.Compare(value, other.value);

    public override bool Equals(object obj) => Equals(obj as CaseToleranceStringKey);

    public override int GetHashCode() => Comparer.GetHashCode(value);

    public static bool operator==(CaseToleranceStringKey? left, CaseToleranceStringKey? right) => Equals(left, right);

    public static bool operator!=(CaseToleranceStringKey? left, CaseToleranceStringKey? right) => !(left == right);

    #endregion
}