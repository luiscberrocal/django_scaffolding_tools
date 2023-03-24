import re
from abc import ABC, abstractmethod
from typing import Dict, Any, List

from django_scaffolding_tools.django.utils import get_max_length


class ModelFieldHandler(ABC):
    @abstractmethod
    def set_next(self, handler: 'ModelFieldHandler') -> 'ModelFieldHandler':
        pass

    @abstractmethod
    def handle(self, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        pass
class AbstractModelFieldHandler(ModelFieldHandler):
    _next_handler: ModelFieldHandler = None

    def set_next(self, handler: 'ModelFieldHandler') -> 'ModelFieldHandler':
        self._next_handler = handler
        return handler

    def handle(self, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        if self._next_handler:
            return self._next_handler.handle(field_data)
        return None

class IntegerFieldHandler(AbstractModelFieldHandler):
    field = 'IntegerField'
    def __init__(self):
        regexp_str = r'(datetime|timestamp|time)'
        self.regexp = re.compile(regexp_str)

    def handle(self, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        if field_data['data_type'] != self.field:
            return None
        match = self.regexp.match(field_data['name'])
        if match is None:
            value = 'LazyAttribute(lambda o: randint(1, 100))'
        else:
            value = 'LazyAttribute(lambda x: faker.date_time_between(start_date="-1y", ' \
                    'end_date="now", tzinfo=timezone(settings.TIME_ZONE)).timestamp())'
        field_data['factory_field'] = value
        return field_data

class CharField(AbstractModelFieldHandler):
    field = 'CharField'
    def __init__(self):
        regexp_str = r'(id|key)'
        self.regexp = re.compile(regexp_str)

    def handle(self, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        if field_data['data_type'] != self.field:
            return None
        max_length = get_max_length(field_data)
        match = self.regexp.match(field_data['name'])
        if match is None:
            value = f'LazyAttribute(lambda x: FuzzyText(length={max_length}, chars=string.ascii_uppercase).fuzz())'
        else:
            value = f'LazyAttribute(lambda x: FuzzyText(length={max_length}, chars=string.digits).fuzz())'
        field_data['factory_field'] = value
        return field_data



