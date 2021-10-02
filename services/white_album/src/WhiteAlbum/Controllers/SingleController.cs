using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using WhiteAlbum.Authorization;
using WhiteAlbum.Entities;
using WhiteAlbum.Repository;
using WhiteAlbum.Requests;
using Single = WhiteAlbum.Entities.Single;

namespace WhiteAlbum.Controllers
{
    public class SingleController : BaseController
    {
        private readonly SingleRepository singleRepository;

        public SingleController(
            SingleRepository singleRepository, 
            IAuthorizationProvider authorizationProvider) : base(authorizationProvider)
        {
            this.singleRepository = singleRepository;
        }

        [HttpPost("single/create")]
        public async Task Create([FromBody] CreateSingleRequest request)
        {
            await singleRepository.Create(request);
        }

        [HttpPost("single/get")]
        public async Task<Single> Get([FromBody] GetSingleRequest request)
        {
            var single = await singleRepository.Get(request.Id);

            single.ShouldBeOwned();

            return single;
        }
        
        [HttpPost("single/get_by_date")]
        public async Task<SingleEntry[]> GetRecent([FromBody] GetByDateRequest request)
        {
            return await singleRepository.GetByDate(request);
        }
    }
}