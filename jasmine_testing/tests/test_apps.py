from django.apps import apps
from django.test import TestCase
from jasmine_testing.apps import JasmineTestingConfig


class TestJasmineConfig(TestCase):

    def test_app(self):
        self.assertEqual('jasmine_testing', JasmineTestingConfig.name)
        self.assertEqual('jasmine_testing',
                         apps.get_app_config('jasmine_testing').name)
