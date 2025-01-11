import re
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

from django_scaffolding_tools.django.utils import get_max_length, get_decimal_info


class ModelFieldHandler(ABC):
    @abstractmethod
    def set_next(self, handler: "ModelFieldHandler") -> "ModelFieldHandler":
        pass

    @abstractmethod
    def handle(self, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        pass


class AbstractModelFieldHandler(ModelFieldHandler):
    _next_handler: ModelFieldHandler = None
    field = None
    _next_handlers = list()
    _current_index = 0

    def set_next(self, handler: "ModelFieldHandler") -> "ModelFieldHandler":
        self._next_handler = handler
        return handler

    def handle(self, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        if self._next_handler is not None:
            return self._next_handler.handle(field_data)
        return None

    def __iter__(self):
        self._next_handlers = list()
        self._current_index = 0
        my_next = self._next_handler
        self._next_handlers.append(my_next)
        while True:
            my_next = my_next._next_handler
            if my_next is None:
                break
            self._next_handlers.append(my_next)
        for handler in self._next_handlers:
            yield handler

    def __len__(self):
        self.__iter__()
        return len(self._next_handlers)


class DateTimeFieldHandler(AbstractModelFieldHandler):
    field = "DateTimeField"

    def handle(self, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        if field_data["data_type"] == self.field:
            field_data["factory_field"] = (
                'LazyAttribute(lambda x: faker.date_time_between(start_date="-1y", '
                'end_date="now", tzinfo=timezone(settings.TIME_ZONE)))'
            )
            return field_data
        else:
            return super().handle(field_data)


class DateFieldHandler(AbstractModelFieldHandler):
    field = "DateField"

    def handle(self, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        if field_data["data_type"] == self.field:
            field_data["factory_field"] = (
                'LazyAttribute(lambda x: faker.date_time_between(start_date="-1y", '
                'end_date="now", tzinfo=timezone(settings.TIME_ZONE)).date())'
            )
            return field_data
        else:
            return super().handle(field_data)


class ForeignKeyFieldHandler(AbstractModelFieldHandler):
    field = "ForeignKey"

    def handle(self, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        if field_data["data_type"] == self.field:
            class_name = field_data["arguments"][0]["value"]  # FIXME very flaky
            value = f"SubFactory({class_name}Factory)"
            field_data["factory_field"] = value
            return field_data
        else:
            return super().handle(field_data)


class IntegerFieldHandler(AbstractModelFieldHandler):
    field = "IntegerField"

    def __init__(self):
        regexp_str = r".*(datetime|timestamp|time).*"
        self.regexp = re.compile(regexp_str)

    def handle(self, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        if field_data["data_type"] == self.field:
            match = self.regexp.match(field_data["name"])
            if match is None:
                value = "LazyAttribute(lambda o: randint(1, 100))"
            else:
                value = (
                    'LazyAttribute(lambda x: faker.date_time_between(start_date="-1y", '
                    'end_date="now", tzinfo=timezone(settings.TIME_ZONE)).timestamp())'
                )
            field_data["factory_field"] = value
            return field_data
        else:
            return super().handle(field_data)


class CharFieldHandler(AbstractModelFieldHandler):
    field = "CharField"

    def __init__(self):
        regexp_str = r".*(id|key|number).*"
        self.regexp = re.compile(regexp_str)

    def handle(self, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        if field_data["data_type"] == self.field:
            max_length = get_max_length(field_data)
            match = self.regexp.match(field_data["name"])
            if match is None:
                value = f"LazyAttribute(lambda x: FuzzyText(length={max_length}, chars=string.ascii_uppercase).fuzz())"
            else:
                value = f"LazyAttribute(lambda x: FuzzyText(length={max_length}, chars=string.digits).fuzz())"
            field_data["factory_field"] = value
            return field_data
        else:
            return super().handle(field_data)


class DecimalFieldHandler(AbstractModelFieldHandler):
    field = "DecimalField"

    def __init__(self, min_value: str = "25.00", max_value: str = "500.00"):
        self.min_value = min_value
        self.max_value = max_value

    def handle(self, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        if field_data["data_type"] == self.field:
            max_digits, decimal_places = get_decimal_info(field_data)
            value = (
                f"LazyAttribute(lambda x: faker.pydecimal(left_digits={max_digits - decimal_places}, "
                f"right_digits={decimal_places}, "
                f"positive=True, min_value={self.min_value}, max_value={self.max_value}))"
            )
            field_data["factory_field"] = value
            return field_data
        else:
            return super().handle(field_data)


class BooleanFieldHandler(AbstractModelFieldHandler):
    field = "BooleanField"

    def handle(self, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        if field_data["data_type"] == self.field:
            value = "Iterator([True, False])"
            field_data["factory_field"] = value
            return field_data
        else:
            return super().handle(field_data)


class DateTimeCharFieldHandler(AbstractModelFieldHandler):
    field = "CharField"

    def __init__(self):
        regexp_str = r".*(datetime|date|time).*"
        self.regexp = re.compile(regexp_str)
        self.date_format = "%Y-%m-%dT%H:%M:%S%z"

    def handle(self, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        if field_data["data_type"] == self.field:
            match = self.regexp.match(field_data["name"])
            if match is not None:
                value = (
                    f'LazyAttribute(lambda x: faker.date_time_between(start_date="-1y", '
                    f'end_date="now", tzinfo=timezone(settings.TIME_ZONE)).strftime({self.date_format}))'
                )
            else:
                return super().handle(field_data)
            field_data["factory_field"] = value
            return field_data
        else:
            return super().handle(field_data)


class EmailFieldHandler(AbstractModelFieldHandler):
    field = "EmailField"

    def handle(self, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        if field_data["data_type"] == self.field:
            field_data["factory_field"] = f"LazyAttribute(lambda x: faker.ascii_free_email())"
            return field_data
        else:
            return super().handle(field_data)


class JSONFieldHandler(AbstractModelFieldHandler):
    field = "JSONField"

    def handle(self, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        if field_data["data_type"] == self.field:
            field_data["factory_field"] = f"LazyAttribute(lambda x: faker.pydict(5, value_types=[str, int, float]))"
            return field_data
        else:
            return super().handle(field_data)
