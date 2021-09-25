using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using WhiteAlbum.Authorization;
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

        [HttpGet("single/get")]
        public async Task<Single> Get([FromBody] GetSingleRequest request)
        {
            var single = await singleRepository.Get(request.Id);

            await Authorize().For(single).By(Permission.Read);

            return single;
        }

        [HttpGet("single/mix")]
        public async Task<Stream> Mix([FromBody] MixSingleRequest request)
        {
            var single = await singleRepository.Get(request.Id);

            await Authorize().For(single).By(Permission.Read);
            
            throw new NotImplementedException(); // todo mix here
        }
    }
}