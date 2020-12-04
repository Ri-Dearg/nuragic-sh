from django.test import TestCase

from contact.models import Email, EmailHistory, Newsletter


class TestCheckoutModels(TestCase):
    """Tests the models for the checkout app."""

    def setUp(self):
        Newsletter.objects.create(name='basic')

    def test_email_creation_and_string(self):
        """Tests the string method for the model."""
        # A valid email dictionary
        email = {'email': 'test@test.com',
                 'name': 'fname lname',
                 'subject': 'interesting',
                 'message': 'this is a message'}

        # Posts the email, retrieves the email object and confirms the string
        self.client.post('/contact/', email)
        new_email = Email.objects.latest('date')
        self.assertTrue(new_email.message == 'this is a message')
        self.assertEqual(str(new_email), 'test@test.com, interesting')

    def test_newsletter_string(self):
        newsletter = Newsletter.objects.get(name='basic')
        self.assertEqual(str(newsletter), "basic")

    def test_emailhistory_and_newsletter_setting(self):
        # A valid email dictionary
        email1 = {'email': 'test@test.com',
                  'name': 'fname lname',
                  'subject': 'interesting',
                  'message': 'this is a message'}

        # Posts the email, retrieves the email object and confirms the string
        self.client.post('/contact/', email1)
        new_email = Email.objects.latest('date')

        newsletter = Newsletter.objects.get(name='basic')
        newsletter.email_list.append(new_email.email)
        newsletter.save()

        self.client.post('/contact/', email1)

        email_history = EmailHistory.objects.get(
            email_address=new_email.email)
        email_history.save()

        EmailHistory.objects.create(email="second@fake.com")
        newsletter.save()

        self.assertEqual(str(email_history), 'test@test.com')
