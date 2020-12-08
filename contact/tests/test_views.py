from django.test import TestCase

from contact.models import Newsletter


class TestContactViews(TestCase):

    def setUp(self):
        Newsletter.objects.create(name="basic")

    """Tests views for the Email app."""
    # Confirms the correct template is used

    def test_contact_template(self):
        self.client.get('/contact/')
        self.assertTemplateUsed('contact_form.html')

    def test_newsletter_signup(self):
        self.client.post('/contact/f/newsletter/', {'email_en': 'test@test.com'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        newsletter = Newsletter.objects.get(name="basic")

        self.assertTrue("test@test.com" in newsletter.email_list_en)

        response = self.client.post('/contact/f/newsletter/',
                                    {'email_en': 'test@test.com'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertTrue(response.content,
                        {"message": "You have already signed up for the newsletter.",  # NOQA E501
                         "tag": "info"})

        response = self.client.get('/contact/f/newsletter/',
                                   {'email_en': 'test@test.com'},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)
