from typing import Type

from fastapi import Depends, status
from fastapi.responses import JSONResponse
from mountaineer import (
    APIException,
    ControllerBase,
    CoreDependencies,
    Metadata,
    RenderBase,
    passthrough,
)
from mountaineer.database import DatabaseDependencies
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from slopes.plugins.auth.authorize import authorize_response
from slopes.plugins.auth.config import AuthConfig
from slopes.models import User


class SignupRender(RenderBase):
    post_signup_redirect: str
    recapcha_enabled: bool
    recapcha_client_key: str | None


class SignupRequest(BaseModel):
    username: EmailStr
    password: str
    recapcha_key: str | None


class SignupInvalid(APIException):
    status_code = 401
    invalid_reason: str


class SignupController(ControllerBase):
    url = "/auth/signup"
    view_path = ("/app/auth/signup/page.tsx")

    # Defaults to 24 hours
    token_expiration_minutes: int = 60 * 24

    def __init__(self, post_signup_redirect: str, user_model: Type[User] = User):
        super().__init__()
        self.user_model = user_model
        self.post_signup_redirect = post_signup_redirect

    def render(
        self,
        auth_config: AuthConfig = Depends(
            CoreDependencies.get_config_with_type(AuthConfig)
        ),
    ) -> SignupRender:
        return SignupRender(
            post_signup_redirect=self.post_signup_redirect,
            recapcha_enabled=auth_config.RECAPTCHA_ENABLED,
            recapcha_client_key=auth_config.RECAPTCHA_GCP_CLIENT_KEY,
            metadata=Metadata(title="Signup"),
        )

    @passthrough(exception_models=[SignupInvalid])
    async def signup(
        self,
        signup_payload: SignupRequest,
        auth_config: AuthConfig = Depends(
            CoreDependencies.get_config_with_type(AuthConfig)
        ),
        session: AsyncSession = Depends(DatabaseDependencies.get_db_session),
    ):
        # If recapcha is enabled, we require the key
        if auth_config.RECAPTCHA_ENABLED and signup_payload.recapcha_key is None:
            raise SignupInvalid(invalid_reason="Recapcha is required.")

        matched_users = select(self.user_model).where(
            self.user_model.email == signup_payload.username
        )
        result = await session.execute(matched_users)
        user = result.scalars().first()
        if user is not None:
            raise SignupInvalid(invalid_reason="User already exists with this email.")

        # Create a new user
        hashed_password = self.user_model.get_password_hash(signup_payload.password)

        new_user = self.user_model(
            email=signup_payload.username, hashed_password=hashed_password
        )
        session.add(new_user)
        await session.commit()

        response = JSONResponse(content=[], status_code=status.HTTP_200_OK)
        response = authorize_response(
            response,
            user_id=new_user.id,
            auth_config=auth_config,
            token_expiration_minutes=self.token_expiration_minutes,
        )

        return response