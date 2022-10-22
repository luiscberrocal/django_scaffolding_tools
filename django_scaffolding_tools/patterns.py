import re
from functools import partial
from typing import List, Pattern

from django_scaffolding_tools.enums import PatternType


def get_pattern_type(value: str, patterns: List[Pattern], expected_pattern: PatternType) -> Pattern:
    for pattern in patterns:
        if pattern.match(value):
            return expected_pattern


EMAIL_PATTERNS = [
    re.compile(
        r'^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))'
        r'([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$')
]
URL_PATTERNS = [
    re.compile(
        r'^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)')
]

get_email_pattern = partial(get_pattern_type, patterns=EMAIL_PATTERNS, expected_pattern=PatternType.EMAIL)
get_url_pattern = partial(get_pattern_type, patterns=URL_PATTERNS, expected_pattern=PatternType.URL)

PATTERN_FUNCTIONS = [get_email_pattern, get_url_pattern]
