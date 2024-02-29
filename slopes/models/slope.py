
from mountaineer.database import SQLModel, Field

class SlopeItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    description: str
