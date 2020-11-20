from django.apps import apps
from django.test import TestCase
from info.apps import InfoConfig


class TestJasmineConfig(TestCase):

    def test_app(self):
        self.assertEqual('info', InfoConfig.name)
        self.assertEqual('info',
                         apps.get_app_config('info').name)
