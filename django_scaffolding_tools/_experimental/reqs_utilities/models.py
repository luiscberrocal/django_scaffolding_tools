from datetime import datetime

from pydantic import BaseModel, Field


class RecommendedRequirement(BaseModel):
    name: str
    latest_version: str
    approved_version: str
    group: str
    last_updated: datetime = Field(default=datetime.now())
