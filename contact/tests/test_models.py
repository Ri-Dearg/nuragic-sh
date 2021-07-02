"""Tests for the Contact app Models."""
from contact.models import Email, EmailHistory, Newsletter
from django.shortcuts import reverse
from django.test import TestCase


class TestContactModels(TestCase):
    """Tests the models for the Contact app."""

    def setUp(self):
        Newsletter.objects.create(name='basic')

    def test_email_creation_and_string(self):
        """Tests the emails are correctly created for the model."""
        # A valid email dictionary
        email = {'email': 'test@test.com',
                 'name': 'fname lname',
                 'subject': 'interesting',
                 'message': 'this is a message'}

        # Posts the email, retrieves the email object and confirms the string
        self.client.post(reverse('contact:email-form'), email)
        new_email = Email.objects.latest('date')
        self.assertTrue(new_email.message == 'this is a message')
        self.assertEqual(str(new_email), 'test@test.com, interesting')

        self.client.post(reverse('contact:email-form'),
                         email, HTTP_ACCEPT_LANGUAGE='it')
        new_email = Email.objects.latest('date')
        self.assertTrue(new_email.message == 'this is a message')
        self.assertEqual(str(new_email), 'test@test.com, interesting')

    def test_newsletter_string(self):
        """Tests the string method on the Newsletter."""
        newsletter = Newsletter.objects.filter(
            name='basic').order_by('id').first()
        self.assertEqual(str(newsletter), "basic")

    def test_emailhistory_and_newsletter_setting(self):
        """Tests contact models creation and saving, str method"""
        email1 = {'email': 'test@test.com',
                  'name': 'fname lname',
                  'subject': 'interesting',
                  'message': 'this is a message'}

        email2 = {'email': 'test2@test.com',
                  'name': 'fname lname',
                  'subject': 'interesting',
                  'message': 'this is a message'}

        # Posts the English email, creating an email for use in the tests
        self.client.post(reverse('contact:email-form'), email1)
        new_email1 = Email.objects.latest('date')

        newsletter = Newsletter.objects.filter(
            name='basic').order_by('id').first()

        # Adds the email address to the English newsletter
        newsletter.email_list_en.append(new_email1.email)
        newsletter.save()

        # Posts the Italian email, creating an email for use in the tests
        self.client.post(reverse('contact:email-form'),
                         email2, HTTP_ACCEPT_LANGUAGE='it')
        new_email2 = Email.objects.latest('date')

        # Adds the email address to the Italian newsletter
        newsletter.email_list_it.append(new_email2.email)
        newsletter.save()

        # Posts an email in both languages
        self.client.post(reverse('contact:email-form'),
                         email1, HTTP_ACCEPT_LANGUAGE='en')
        self.client.post(reverse('contact:email-form'),
                         email2, HTTP_ACCEPT_LANGUAGE='it')

        # Saves emails into Email history
        email_history1 = EmailHistory.objects.get(
            email_address=new_email1.email)
        email_history1.save()

        email_history2 = EmailHistory.objects.get(
            email_address=new_email2.email)
        email_history2.save()

        EmailHistory.objects.create(email="second@fake.com")
        newsletter.save()

        self.assertEqual(str(email_history1), 'test@test.com')
        self.assertEqual(str(email_history2), 'test2@test.com')
