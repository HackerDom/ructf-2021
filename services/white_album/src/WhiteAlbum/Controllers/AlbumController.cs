using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using WhiteAlbum.Authorization;
using WhiteAlbum.Entities;
using WhiteAlbum.Repository;
using WhiteAlbum.Requests;
using Single = WhiteAlbum.Entities.Single;

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
        
        [HttpPost("album/get")]
        public async Task<Album> GetAlbum([FromBody] GetAlbumRequest request)
        {
            var album = await albumRepository.Get(request.Id);
            
            await Authorize().For(album).By(Permission.Read);

            return album;
        }
        
        [HttpPost("album/get_all_singles")]
        public async Task<Single[]> GetAllSingles([FromBody] GetAllSinglesRequest request)
        {
            var album = await albumRepository.Get(request.Id);
        
            await Authorize().For(album).By(Permission.Read);
        
            var result = new List<Single>();
        
            foreach (var singleId in album.Singles)
            {
                result.Add(await singleRepository.Get(singleId));
            }
            
            return result.ToArray();
        }
        
        [HttpPost("album/get_by_date")]
        public async Task<AlbumEntry[]> GetRecent([FromBody] GetByDateRequest request)
        {
            return await albumRepository.GetByDate(request);
        }
        
        [HttpPost("album/attach")]
        public async Task AttachToAlbum([FromBody] AttachSingleToAlbumRequest request)
        {
            var single = await singleRepository.Get(request.Single);
            var album = await albumRepository.Get(request.AlbumId);

            await Authorize()
                .For(single)
                .And(album)
                .By(Permission.Write);
            
            await albumRepository.Attach(single, album);
        }
    }
}