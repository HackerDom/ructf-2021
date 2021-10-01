using System.Linq;
using Microsoft.AspNetCore.Mvc.ApplicationParts;
using Microsoft.AspNetCore.Mvc.Controllers;
using Microsoft.Extensions.DependencyInjection;

namespace WhiteAlbum
{
    internal static class ServiceCollectionExtensions
    {
        public static void DiscoverInternalControllers(this IServiceCollection services)
        {
            var applicationPartManager = (ApplicationPartManager) services.First(d => d.ServiceType == typeof (ApplicationPartManager)).ImplementationInstance;
            var oldControllerFeatureProvider = applicationPartManager.FeatureProviders.OfType<ControllerFeatureProvider>().First();
            var newControllerFeatureProvider = new InternalControllerFeatureProvider();

            applicationPartManager.FeatureProviders.Remove(oldControllerFeatureProvider);
            applicationPartManager.FeatureProviders.Add(newControllerFeatureProvider);
        }
    }
}