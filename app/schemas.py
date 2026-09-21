from pydantic import BaseModel
from pydantic import Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_lengt=100)
    description: str | None = None


class ProjectResponse(BaseModel):
    id: int
    name: str = Field(min_length=1, max_lengt=100)
    description: str | None = None

