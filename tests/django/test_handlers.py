import json

from django_scaffolding_tools.django.handlers import IntegerFieldHandler, DateFieldHandler, DateTimeFieldHandler, \
    CharFieldHandler, ForeignKeyFieldHandler, DecimalFieldHandler, BooleanFieldHandler, DateTimeCharFieldHandler


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

    int_handler = IntegerFieldHandler()
    char_handler = CharFieldHandler()

    int_handler.set_next(char_handler)

    result = int_handler.handle(field_data)
    expected = 'LazyAttribute(lambda x: FuzzyText(length=64, chars=string.digits).fuzz())'
    assert result['factory_field'] == expected


def test_date_time_char_handler():
    field_list = [{
        "name": "payment_date",
        "keywords": [
            {
                "name": "max_length",
                "value_type_TMP": "Constant",
                "value": 15
            }
        ],
        "arguments": [],
        "data_type": "CharField"
    },
    {
        "name": "payment_id",
        "keywords": [
            {
                "name": "max_length",
                "value_type_TMP": "Constant",
                "value": 16
            }
        ],
        "arguments": [],
        "data_type": "CharField"
    }
    ]

    handlers = [
        DateTimeCharFieldHandler(),
        CharFieldHandler()
    ]

    for i in range(len(handlers)):
        if i < len(handlers) - 1:
            handlers[i].set_next(handlers[i + 1])

    handler = handlers[0]
    expected_values = [
        'LazyAttribute(lambda x: faker.date_time_between(start_date="-1y", '
        'end_date="now", tzinfo=timezone(settings.TIME_ZONE)).strftime(%Y-%m-%dT%H:%M:%S%z))',
        'LazyAttribute(lambda x: FuzzyText(length=16, chars=string.digits).fuzz())'
    ]
    for i, field_data in enumerate(field_list):
        result = handler.handle(field_data)
        assert result['factory_field'] == expected_values[i] #, f'assertion error with {field_data["name"]}'


def test_all(fixtures_folder, output_folder):
    file = fixtures_folder / 'model_data_models_payements.py.json'
    file = output_folder / 'django' / 'model_data_models.py.json'

    with open(file, 'r') as json_file:
        class_data = json.load(json_file)
    handlers = [
        IntegerFieldHandler(),
        DateTimeCharFieldHandler(),
        CharFieldHandler(),
        ForeignKeyFieldHandler(),
        DateFieldHandler(),
        DateTimeFieldHandler(),
        DecimalFieldHandler(),
        BooleanFieldHandler()
    ]

    for i in range(len(handlers)):
        if i < len(handlers) - 1:
            handlers[i].set_next(handlers[i + 1])
    print('----------------------------------------------------------')
    main_handler = handlers[0]
    for fp_data in class_data['classes']:
        # fp_data = class_data['classes'][3]
        print(f'class {fp_data["name"]}Factory(DjangoModelFactory):')
        print(f'\tclass Meta:')
        print(f'\t\tmodel = {fp_data["name"]}')
        print("")
        for att in fp_data['attributes']:
            result = main_handler.handle(att)
            if result is None:
                print(f'\t# {att["name"]} {att["data_type"]} NOT supported')
            else:
                print(f'\t{result["name"]} = {result["factory_field"]}')
        print("#" * 80)


def test_iteration():
    handlers = [
        IntegerFieldHandler(),
        DateTimeCharFieldHandler(),
        CharFieldHandler(),
        ForeignKeyFieldHandler(),
        DateFieldHandler(),
        DateTimeFieldHandler(),
        DecimalFieldHandler(),
        BooleanFieldHandler()
    ]

    for i in range(len(handlers)):
        if i < len(handlers) - 1:
            handlers[i].set_next(handlers[i + 1])

    main_handler = handlers[0]
    for handler in main_handler:
        print(f'{handler.__class__.__name__} {handler.field}')

    handler_list = list(main_handler)
    print(handler_list)
