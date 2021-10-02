using System.Threading.Tasks;
using WhiteAlbum.Entities;

namespace WhiteAlbum.Authorization
{
    public interface IAuthorizationRequestBuilder
    {
        IAuthorizationRequestBuilder For(Single single);
        IAuthorizationRequestBuilder For(Album album);
        
        IAuthorizationRequestBuilder And(Single single);
        IAuthorizationRequestBuilder And(Album album);

        Task BySuperAdministratorAccess();
        Task<bool> HasSuperAdministratorAccess();
        Task By(Permission role);
    }
}