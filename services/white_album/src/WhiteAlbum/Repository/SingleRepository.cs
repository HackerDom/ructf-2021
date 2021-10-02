using System;
using System.Threading.Tasks;
using WhiteAlbum.Entities;
using WhiteAlbum.Requests;
using WhiteAlbum.Stores;
using Single = WhiteAlbum.Entities.Single;

namespace WhiteAlbum.Repository
{
    public class SingleRepository
    {
        private readonly SingleStore singleStore;

        public SingleRepository(SingleStore singleStore)
        {
            this.singleStore = singleStore;
        }

        public async Task<Single> Get(SingleId singleId)
        {
            return await singleStore.Get(singleId);
        }

        public async Task Create(CreateSingleRequest request)
        {
            await singleStore.Create(request);
        }
        
        public async Task<SingleEntry[]> GetByDate(GetByDateRequest request)
        {
            return await singleStore.GetByDate(request.Date);
        }
    }
}