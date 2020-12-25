from contact.models import Newsletter
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from info.models import Category


class TestContactViews(TestCase):

    def setUp(self):
        image = SimpleUploadedFile(
            name='default.jpg',
            content=open(
                'media/default.jpg',
                 'rb').read(),
            content_type='image/jpeg',)
        Newsletter.objects.create(name="basic")
        valid_category = Category(title_en='about',
                                  title_it='about',
                                  menu_word_en='HCMW1',
                                  menu_word_it='HCMW1',
                                  description_en='description',
                                  description_it='description',
                                  image=image,
                                  button_text="text here",
                                  order=1)
        valid_category.save()

    """Tests views for the Email app."""
    # Confirms the correct template is used

    def test_contact_template(self):
        self.client.get('/contact/')
        self.assertTemplateUsed('contact_form.html')

    def test_newsletter_signup(self):
        self.client.post('/contact/f/newsletter/',
                         {'email_en': 'test@test.com'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.client.post('/it/contact/f/newsletter/',
                         {'email_it': 'test@test.com'},
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
