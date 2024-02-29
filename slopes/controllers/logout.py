from fastapi import Depends, status
from mountaineer import (
    ControllerBase,
    Metadata,
    RenderBase,
)
from starlette.responses import RedirectResponse

from slopes.plugins.auth.dependencies import AuthDependencies


class LogoutController(ControllerBase):
    url = "/auth/logout"
    view_path = ("/app/auth/logout/page.tsx")

    def __init__(self, post_logout_redirect: str):
        super().__init__()
        self.post_logout_redirect = post_logout_redirect

    def render(
        self,
        access_token_cookie_key: str = Depends(AuthDependencies.access_token_cookie_key),
    ) -> RenderBase:
        response = RedirectResponse(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            url=self.post_logout_redirect,
        )

        # Remove the cookies
        print("REMOVE COOKIE", access_token_cookie_key)
        response.delete_cookie(access_token_cookie_key, path="/", httponly=True)
        
        return RenderBase(
            metadata=Metadata(title="Logout", explicit_response=response),
        )