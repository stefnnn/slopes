
from uuid import UUID

from mountaineer import Metadata, RenderBase, ControllerBase, APIException, sideeffect
from mountaineer.database import DatabaseDependencies

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

from slopes import models
from slopes.models.user import User
from slopes.plugins.auth.dependencies import AuthDependencies

class NotFoundException(APIException):
    status_code = 404
    slope = "Slope not found"


class UpdateTextRequest(BaseModel):
    description: str


class SlopeRender(RenderBase):
    id: int
    description: str


class SlopeController(ControllerBase):
    url = "/slope/{slope_id}/"
    view_path = "/app/slope/page.tsx"

    def __init__(self):
        super().__init__()

    async def render(
        self,
        slope_id: int,
        session: AsyncSession = Depends(DatabaseDependencies.get_db_session),
        _user: User = Depends(AuthDependencies.require_valid_user(User))
    ) -> SlopeRender:
        slope_item = await session.get(models.SlopeItem, slope_id)

        if not slope_item:
            raise NotFoundException()

        return SlopeRender(
            id=slope_item.id,
            description=slope_item.description,
            metadata=Metadata(title=f"Slope: {slope_id}"),
        )

    @sideeffect
    async def update_text(
        self,
        slope_id: int,
        payload: UpdateTextRequest,
        session: AsyncSession = Depends(DatabaseDependencies.get_db_session)
    ):
        slope_item = await session.get(models.SlopeItem, slope_id)
        if not slope_item:
            raise NotFoundException()

        slope_item.description = payload.description
        await session.commit()
