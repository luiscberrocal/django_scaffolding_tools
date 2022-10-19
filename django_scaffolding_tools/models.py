from typing import List, Optional, Union

from pydantic import BaseModel


class Keyword(BaseModel):
    name: str
    value: Union[int, str]


class Serializer(BaseModel):
    field_type: str
    keywords: List[Keyword]


class Attribute(BaseModel):
    name: str
    value: str
    supported: bool
    native: bool
    alias: Optional[str] = None
    data_type: str
    length: int
    serializer: Serializer


class Model(BaseModel):
    name: str
    level: int
    attributes: List[Attribute]
