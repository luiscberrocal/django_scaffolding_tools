import re
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

from django_scaffolding_tools.django.utils import get_max_length, get_decimal_info


class ModelFieldHandler(ABC):
    @abstractmethod
    def set_next(self, handler: 'ModelFieldHandler') -> 'ModelFieldHandler':
        pass

    @abstractmethod
    def handle(self, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        pass


class AbstractModelFieldHandler(ModelFieldHandler):
    _next_handler: ModelFieldHandler = None
    field = None

    def set_next(self, handler: 'ModelFieldHandler') -> 'ModelFieldHandler':
        self._next_handler = handler
        return handler

    def handle(self, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        if self._next_handler:
            return self._next_handler.handle(field_data)
        return None


class DateTimeFieldHandler(AbstractModelFieldHandler):
    field = 'DateTimeField'

    # field = 'CharField'

    def handle(self, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        if field_data['data_type'] == self.field:
            field_data['factory_field'] = f'{self.field} Not supported'
            return field_data
        else:
            return super().handle(field_data)


class DateFieldHandler(AbstractModelFieldHandler):
    field = 'DateField'

    def handle(self, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        if field_data['data_type'] == self.field:
             field_data['factory_field'] = f'{self.field} Not supported'
             return field_data
        else:
            return super().handle(field_data)


class ForeignKeyFieldHandler(AbstractModelFieldHandler):
    field = 'ForeignKey'

    def handle(self, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        if field_data['data_type'] == self.field:
            class_name = field_data['arguments'][0]['value']  # FIXME very flaky
            value = f'SubFactory({class_name}Factory)'
            field_data['factory_field'] = value
            return field_data
        else:
            return super().handle(field_data)


class IntegerFieldHandler(AbstractModelFieldHandler):
    field = 'IntegerField'

    def __init__(self):
        regexp_str = r'.*(datetime|timestamp|time).*'
        self.regexp = re.compile(regexp_str)

    def handle(self, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        if field_data['data_type'] == self.field:
            match = self.regexp.match(field_data['name'])
            if match is None:
                value = 'LazyAttribute(lambda o: randint(1, 100))'
            else:
                value = 'LazyAttribute(lambda x: faker.date_time_between(start_date="-1y", ' \
                        'end_date="now", tzinfo=timezone(settings.TIME_ZONE)).timestamp())'
            field_data['factory_field'] = value
            return field_data
        else:
            return super().handle(field_data)


class CharFieldHandler(AbstractModelFieldHandler):
    field = 'CharField'

    def __init__(self):
        regexp_str = r'.*(id|key).*'
        self.regexp = re.compile(regexp_str)

    def handle(self, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        if field_data['data_type'] == self.field:
            max_length = get_max_length(field_data)
            match = self.regexp.match(field_data['name'])
            if match is None:
                value = f'LazyAttribute(lambda x: FuzzyText(length={max_length}, chars=string.ascii_uppercase).fuzz())'
            else:
                value = f'LazyAttribute(lambda x: FuzzyText(length={max_length}, chars=string.digits).fuzz())'
            field_data['factory_field'] = value
            return field_data
        else:
            return super().handle(field_data)


class DecimalFieldHandler(AbstractModelFieldHandler):
    field = 'DecimalField'

    def __init__(self, min_value: str = '25.00', max_value: str = '500.00'):
        self.min_value = min_value
        self.max_value = max_value

    def handle(self, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        if field_data['data_type'] == self.field:
            max_digits, decimal_places = get_decimal_info(field_data)
            value = f'LazyAttribute(lambda x: faker.pydecimal(left_digits={max_digits - decimal_places}, ' \
                    f'right_digits={decimal_places}, ' \
                    f'positive=True, min_value={self.min_value}, max_value={self.max_value}))'
            field_data['factory_field'] = value
            return field_data
        else:
            return super().handle(field_data)
