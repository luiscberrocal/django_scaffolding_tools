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
    EMAIL = 'email'
    URL = 'url'
    DATETIME = 'datetime'
    DATE = 'date'
