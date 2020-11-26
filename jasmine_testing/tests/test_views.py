from django.test import TestCase
from django.contrib.auth.models import User


class TestJasmineViews(TestCase):

    def test_render_jasmine(self):
        response = self.client.get('/jasmine/')
        self.assertEqual(response.status_code, 500)

        password = 'mypassword'
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com',
                                                 password)
        self.client.login(username=my_admin.username, password=password)

        response = self.client.get('/jasmine/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'jasmine_testing/jasmine.html')
