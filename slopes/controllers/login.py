from typing import Type

from fastapi import Depends, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from mountaineer import (
    APIException,
    ControllerBase,
    CoreDependencies,
    Metadata,
    RenderBase,
    passthrough,
)
from mountaineer.database import DatabaseDependencies
from mountaineer.dependencies import get_function_dependencies
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from slopes.plugins.auth.authorize import authorize_response
from slopes.plugins.auth.config import AuthConfig
from slopes.plugins.auth.dependencies import AuthDependencies
from slopes.models import User


class LoginRequest(BaseModel):
    username: EmailStr
    password: str


class LoginInvalid(APIException):
    status_code = 401
    invalid_reason: str


class LoginRender(RenderBase):
    post_login_redirect: str


class LoginController(ControllerBase):
    """
    Clients can override this login controller to instantiate their own login / view conventions.
    """

    url = "/auth/login"
    view_path = ("/app/auth/login/page.tsx")

    # Defaults to 24 hours
    token_expiration_minutes: int = 60 * 24

    def __init__(
        self,
        post_login_redirect: str,
        user_model: Type[User] = User,
    ):
        super().__init__()
        self.user_model = user_model
        self.post_login_redirect = post_login_redirect

    async def render(
        self,
        request: Request,
        after_login: str | None = None,
    ) -> LoginRender:
        # Workaround to provide user-defined models into the dependency layer
        # since instance variables can't be specified in the Depends() kwarg
        get_dependencies_fn = AuthDependencies.peek_user(self.user_model)
        async with get_function_dependencies(
            callable=get_dependencies_fn, url=self.url, request=request
        ) as values:
            user = await get_dependencies_fn(**values)

        if user is not None:
            # return RedirectResponse(url=self.post_login_redirect, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
            return LoginRender(
                post_login_redirect="",
                metadata=Metadata(
                    explicit_response=RedirectResponse(
                        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
                        url=after_login or self.post_login_redirect,
                    )
                ),
            )

        # Otherwise continue to load the initial page
        return LoginRender(
            post_login_redirect=after_login or self.post_login_redirect,
            metadata=Metadata(title="Login")
        )

    @passthrough(exception_models=[LoginInvalid])
    async def login(
        self,
        login_payload: LoginRequest,
        auth_config: AuthConfig = Depends(
            CoreDependencies.get_config_with_type(AuthConfig)
        ),
        session: AsyncSession = Depends(DatabaseDependencies.get_db_session),
    ):
        matched_users = select(self.user_model).where(
            self.user_model.email == login_payload.username
        )
        results = await session.execute(matched_users)
        user = results.scalars().first()
        if user is None:
            raise LoginInvalid(invalid_reason="User not found.")
        if not user.verify_password(login_payload.password):
            raise LoginInvalid(invalid_reason="Invalid password.")

        response = JSONResponse(content=[], status_code=status.HTTP_200_OK)
        response = authorize_response(
            response,
            user_id=user.id,
            auth_config=auth_config,
            token_expiration_minutes=self.token_expiration_minutes,
        )

        return response