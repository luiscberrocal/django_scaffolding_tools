import os

from django_scaffolding_tools.django.utils import DjangoAppManager


def test_django_loading():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
    app_manager = DjangoAppManager()

