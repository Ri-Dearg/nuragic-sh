"""Tests views for the Contact app."""
from contact.models import Newsletter
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from info.models import Category


class TestContactViews(TestCase):
    """Tests for Contact app views."""

    def setUp(self):
        """Created instances for use in tests"""
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

    def test_contact_template(self):
        """Tests templates for Contact page."""
        self.client.get('/contact/')
        self.assertTemplateUsed('contact_form.html')

    def test_newsletter_singup(self):
        """FETCH method for signing up to newletter checked."""
        # Signs up for newsletter in both languages.
        self.client.post('/contact/f/newsletter/',
                         {'email_en': 'test@test.com'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.client.post('/contact/f/newsletter/',
                         {'email_it': 'test@test.com'},
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                         HTTP_ACCEPT_LANGUAGE='it')

        # Retrieves the newletter and checks that the email is present
        newsletter = Newsletter.objects.get(name="basic")
        self.assertTrue("test@test.com" in newsletter.email_list_en)

        # Checks the correct message is processed if already signed up
        response = self.client.post('/contact/f/newsletter/',
                                    {'email_en': 'test@test.com'},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest',
                                    HTTP_ACCEPT_LANGUAGE='en')
        self.assertTrue(response.content,
                        {"message": "You have already signed up for the newsletter.",  # NOQA E501
                         "tag": "info"})

        # Checks for refusal in a GET request
        response = self.client.get('/contact/f/newsletter/',
                                   {'email_en': 'test@test.com'},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)
