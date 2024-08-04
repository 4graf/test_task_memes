from pydantic import BaseModel, Field


class MemFilterParams(BaseModel):
    page: int = Field(gt=0)
    per_page: int = Field(gt=0)
