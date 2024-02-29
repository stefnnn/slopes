from mountaineer import RenderBase
from pydantic import BaseModel

from slopes.models.user import User

class GlobalState(BaseModel):
    logged_in_user: User | None

class AppRenderer(RenderBase):
    global_state: GlobalState