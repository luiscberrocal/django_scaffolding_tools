import json

from django_scaffolding_tools.django.handlers import IntegerFieldHandler, DateFieldHandler, DateTimeFieldHandler, \
    CharFieldHandler, ForeignKeyFieldHandler


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

def test_all(fixtures_folder):
    file = fixtures_folder / 'model_data_models_payements.py.json'
    with open(file, 'r') as json_file:
        class_data = json.load(json_file)
    fp_data = class_data['classes'][2]
    handlers = [
        IntegerFieldHandler(),
        CharFieldHandler(),
        ForeignKeyFieldHandler(),
        DateFieldHandler(),
        DateTimeFieldHandler()
    ]

    for i in range(len(handlers)):
        if i < len(handlers) - 1:
            print(f'{handlers[i].field} --> {handlers[i+1].field}')
            handlers[i].set_next(handlers[i+1])
    main_handler = handlers[0]
    for att in fp_data['attributes']:
        result = main_handler.handle(att)
        if result is None:
            print(f'{att["name"]} {att["data_type"]} NOT supported')
        else:
            print(f'{result["name"]} = {result["factory_field"]}')
