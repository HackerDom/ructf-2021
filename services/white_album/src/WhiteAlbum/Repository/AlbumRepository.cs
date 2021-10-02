using System.Threading.Tasks;
using WhiteAlbum.Entities;
using WhiteAlbum.Requests;
using WhiteAlbum.Stores;
using Single = WhiteAlbum.Entities.Single;

namespace WhiteAlbum.Repository
{
    public class AlbumRepository
    {
        private readonly AlbumStore albumStore;

        public AlbumRepository(AlbumStore albumStore)
        {
            this.albumStore = albumStore;
        }

        public async Task<Album> Create(CreateAlbumRequest request)
        {
            return await albumStore.Create(request);
        }
        
        public async Task Attach(Single single, Album album)
        {
            await albumStore.AttachSingle(album.Id, single.Id);
        }
        
        public async Task<Album> Get(AlbumId albumId)
        {
            return await albumStore.Get(albumId);
        }

        public async Task Update(UpdateAlbumRequest request)
        { 
            await albumStore.Update(request);
        }

        public async Task<AlbumEntry[]> GetByDate(GetByDateRequest request)
        {
            return await albumStore.GetByDate(request.Date);
        }
    }
}