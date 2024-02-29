
from mountaineer import sideeffect, ControllerBase, Metadata
from mountaineer.database import DatabaseDependencies

from fastapi import Depends, Request
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from slopes import models
from slopes.plugins.auth.dependencies import AuthDependencies
from .app import AppRenderer, GlobalState
from slopes.deps import get_global_state


class HomeRender(AppRenderer):
    items: list[models.SlopeItem]


class HomeController(ControllerBase):
    url = "/"
    view_path = "/app/home/page.tsx"

    async def render(
        self,
        session: AsyncSession = Depends(DatabaseDependencies.get_db_session),
        global_state: GlobalState = Depends(get_global_state),
        user: models.User = Depends(AuthDependencies.peek_user(models.User))
    ) -> HomeRender:
        items = (await session.execute(select(models.SlopeItem))).scalars().all() if user else []
        
        return HomeRender(
            global_state=global_state,
            items=items,
            metadata=Metadata(title="Home"),
        )

    @sideeffect
    async def new_slope(
        self,
        session: AsyncSession = Depends(DatabaseDependencies.get_db_session)
    ):
        obj = models.SlopeItem(description="Untitled Slope")
        session.add(obj)
        await session.commit()
