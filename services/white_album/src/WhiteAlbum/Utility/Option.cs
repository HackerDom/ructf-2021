namespace WhiteAlbum.Utility
{
    public class Option<T> where T: class
    {
        public Option(T? value)
        {
            Value = value;
        }

        public T? Value { get; }
    }
}