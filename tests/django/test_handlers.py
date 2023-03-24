from django_scaffolding_tools.django.handlers import IntegerFieldHandler, DateFieldHandler, DateTimeFieldHandler


class CharFieldHandler:
    pass


def test_handlers():
    field_data = {
        "name": "financial_product_id",
        "keywords": [
            {
                "name": "max_length",
                "value_type_TMP": "Constant",
                "value": 64
            }
        ],
        "arguments": [],
        "data_type": "CharField"
    }
    int_handler = DateFieldHandler()
    char_handler = DateTimeFieldHandler()

    # int_handler = IntegerFieldHandler()
    # char_handler = CharFieldHandler()
    int_handler.set_next(char_handler)
    print(f'Next {char_handler._next_handler}')
    print(f'Next {int_handler._next_handler}')

    result = int_handler.handle(field_data)
    print('>>>', result)

