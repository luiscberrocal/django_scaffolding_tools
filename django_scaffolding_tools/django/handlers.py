import re
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

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
    field = None

    def set_next(self, handler: 'ModelFieldHandler') -> 'ModelFieldHandler':
        self._next_handler = handler
        return handler

    def handle(self, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        if self._next_handler:
            print(f'Calling next {self._next_handler.__class__.__name__}')
            return self._next_handler.handle(field_data)
        return None


class DateTimeFieldHandler(AbstractModelFieldHandler):
    field = 'DateTimeField'

    # field = 'CharField'

    def handle(self, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        if field_data['data_type'] == self.field:
            print(f'Returning from {self.__class__.__name__}')
            return {'test': 'CharField'}
        else:
            print(f'Calling super')
            return super().handle(field_data)


class DateFieldHandler(AbstractModelFieldHandler):
    field = 'DateField'

    def handle(self, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        if field_data['data_type'] == self.field:
            return {'test': 'DateField'}
        else:
            return super().handle(field_data)


class ForeignKeyFieldHandler(AbstractModelFieldHandler):
    field = 'ForeignKey'

    def handle(self, field_data: Dict[str, Any]) -> Dict[str, Any] | None:
        if field_data['data_type'] == self.field:
            class_name = field_data['arguments'][0]['value'] # FIXME very flaky
            value = f'SubFactory({class_name}Factory)'
            field_data['factory_field'] = value
            return field_data
        else:
            print(f'{field_data["data_type"]} != {self.field}')
            return super().handle(field_data)


class IntegerFieldHandler(AbstractModelFieldHandler):
    field = 'IntegerField'

    def __init__(self):
        regexp_str = r'(datetime|timestamp|time)'
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
            print(f'{field_data["data_type"]} != {self.field}')
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


class Handler(ABC):
    """
    The Handler interface declares a method for building the chain of handlers.
    It also declares a method for executing a request.
    """

    @abstractmethod
    def set_next(self, handler: 'Handler') -> 'Handler':
        pass

    @abstractmethod
    def handle(self, request) -> Optional[str]:
        pass


class AbstractHandler(Handler):
    """
    The default chaining behavior can be implemented inside a base handler
    class.
    """

    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        # Returning a handler from here will let us link handlers in a
        # convenient way like this:
        # monkey.set_next(squirrel).set_next(dog)
        return handler

    @abstractmethod
    def handle(self, request: Any) -> str:
        if self._next_handler:
            return self._next_handler.handle(request)

        return None


"""
All Concrete Handlers either handle a request or pass it to the next handler in
the chain.
"""


class MonkeyHandler(AbstractHandler):
    def handle(self, request: Any) -> str:
        if request == "Banana":
            return f"Monkey: I'll eat the {request}"
        else:
            return super().handle(request)


class SquirrelHandler(AbstractHandler):
    def handle(self, request: Any) -> str:
        if request == "Nut":
            return f"Squirrel: I'll eat the {request}"
        else:
            return super().handle(request)


class DogHandler(AbstractHandler):
    def handle(self, request: Any) -> str:
        if request == "MeatBall":
            return f"Dog: I'll eat the {request}"
        else:
            return super().handle(request)


def client_code(handler: Handler) -> None:
    """
    The client code is usually suited to work with a single handler. In most
    cases, it is not even aware that the handler is part of a chain.
    """

    for food in ["Nut", "Banana", "Cup of coffee"]:
        print(f"\nClient: Who wants a {food}?")
        result = handler.handle(food)
        if result:
            print(f"  {result}", end="")
        else:
            print(f"  {food} was left untouched.", end="")


if __name__ == "__main__":
    monkey = MonkeyHandler()
    squirrel = SquirrelHandler()
    dog = DogHandler()

    monkey.set_next(squirrel).set_next(dog)

    # The client should be able to send a request to any handler, not just the
    # first one in the chain.
    print("Chain: Monkey > Squirrel > Dog")
    client_code(monkey)
    print("\n")

    print("Subchain: Squirrel > Dog")
    client_code(squirrel)
