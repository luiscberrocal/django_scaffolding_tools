from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


def convert_datetime_to_iso_8601_with_z_suffix(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')


class RecommendedRequirement(BaseModel):
    name: str
    latest_version: str
    approved_version: str
    group: Optional[str]
    environment: str
    last_updated: datetime = Field(default=datetime.now())

    class Config:
        json_encoders = {
            datetime: convert_datetime_to_iso_8601_with_z_suffix
        }
