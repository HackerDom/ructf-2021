using System.Threading.Tasks;

namespace WhiteAlbum.Authorization
{
    public interface IAuthorizer
    {
        Task By(Permission permission);

        Task<bool> HasAccess(Permission permission);
    }
}