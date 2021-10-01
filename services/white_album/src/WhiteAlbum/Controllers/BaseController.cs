using System;
using Microsoft.AspNetCore.Mvc;
using WhiteAlbum.Authorization;

namespace WhiteAlbum.Controllers
{
    public abstract class BaseController : ControllerBase
    {
        private readonly IAuthorizationProvider authorizationProvider;

        protected BaseController(IAuthorizationProvider authorizationProvider) =>
            this.authorizationProvider = authorizationProvider;

        protected IAuthorizationRequestBuilder Authorize() =>
            new AuthorizationRequestBuilder(authorizationProvider, Context.User ?? throw new UnauthorizedAccessException("Unknown user"));
    }
}