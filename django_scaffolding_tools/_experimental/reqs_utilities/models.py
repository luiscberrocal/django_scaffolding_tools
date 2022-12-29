from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


def convert_datetime_to_iso_8601_with_z_suffix(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')


class RecommendedRequirement(BaseModel):
    name: str
    latest_version: str
    approved_version: str
    group: Optional[str]
    environment: str
    last_updated: datetime = Field(default=datetime.now())
    home_page: Optional[HttpUrl]
    license: Optional[str]

    def to_req_line(self) -> str:
        if self.home_page is None:
            line = f'{self.name}=={self.approved_version}'
        else:
            line = f'{self.name}=={self.approved_version} # {self.home_page}'
        return line

    class Config:
        json_encoders = {
            datetime: convert_datetime_to_iso_8601_with_z_suffix
        }
