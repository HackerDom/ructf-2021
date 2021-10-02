namespace WhiteAlbum.Requests
{
    public class GetByDateRequest
    {
        public GetByDateRequest(Date date)
        {
            Date = date;
        }

        public Date Date { get; }
    }
}