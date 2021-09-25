using System;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using WhiteAlbum.Authorization;
using WhiteAlbum.Entities;
using WhiteAlbum.Repository;
using WhiteAlbum.Requests;

namespace WhiteAlbum.Controllers
{
    public class AlbumController : BaseController
    {
        private readonly AlbumRepository albumRepository;
        private readonly SingleRepository singleRepository;

        public AlbumController(
            AlbumRepository albumRepository,
            SingleRepository singleRepository, 
            IAuthorizationProvider authorizationProvider) : base(authorizationProvider)
        {
            this.albumRepository = albumRepository;
            this.singleRepository = singleRepository;
        }

        [HttpPost("album/create")]
        public async Task CreateAlbum([FromBody] CreateAlbumRequest request)
        {
            await albumRepository.Create(request);
        }
        
        [HttpGet("album/get")]
        public async Task<Album> GetAlbum([FromBody] GetAlbumRequest request)
        {
            var album = await albumRepository.Get(request.Id);

            await Authorize().For(album).By(Permission.Read);

            return album;
        }

        [HttpGet("album/get_recent")]
        public async Task<AlbumEntry[]> GetRecent([FromBody] GetRecentlyCreatedRequest request)
        {
            if (request.Count > 50)
                throw new NotImplementedException();

            return await albumRepository.GetRecentlyCreated(request);
        }
        
        [HttpPost("album/attach")]
        public async Task AttachToAlbum([FromBody] AttachSingleToAlbumRequest request)
        {
            var single = await singleRepository.Get(request.Single);
            var album = await albumRepository.Get(request.AlbumId);

            await Authorize().For(single).And(album).By(Permission.Write);

            await albumRepository.Attach(single, album);
        }
    }
}