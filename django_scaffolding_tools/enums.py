from enum import Enum
from typing import List


class NativeDataType(str, Enum):
    INTEGER = 'int'
    STRING = 'str'
    FLOAT = 'float'
    DATETIME = 'datetime'
    DATE = 'date'

    @classmethod
    def to_list(cls) -> List[str]:
        code_list = [x.value for x in cls]
        return code_list


class PatternType(str, Enum):
    EMAIL = 'email_pattern'
    URL = 'url_pattern'
    DATETIME = 'datetime_pattern'
    DATE = 'date_pattern'


class ASTDataType(str, Enum):
    CLASS = 'ClassDef'
    ASSIGN = 'Assign'
    NAME = 'Name'
    CONSTANT = 'Constant'
    ATTRIBUTE = 'Attribute'
    CALL = 'Call'


class CommandType(str, Enum):
    JSON_TO_SERIALIZER = 'J2SER'
    JSON_TO_DJANGO_MODEL = 'J2DMOD'
