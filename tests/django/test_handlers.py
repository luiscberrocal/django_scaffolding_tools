from django_scaffolding_tools.django.handlers import IntegerFieldHandler, DateFieldHandler, DateTimeFieldHandler, \
    CharFieldHandler


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

    int_handler = IntegerFieldHandler()
    char_handler = CharFieldHandler()

    int_handler.set_next(char_handler)


    result = int_handler.handle(field_data)
    expected = 'LazyAttribute(lambda x: FuzzyText(length=64, chars=string.digits).fuzz())'
    assert result['factory_field'] == expected

