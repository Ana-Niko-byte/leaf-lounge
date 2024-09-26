from django.test import TestCase
from .forms import *


class TestNewsletterForm(TestCase):
    """
    A class for testing the Newsletter Form associated with the Marketing app.
    This form allows users to sign up to the Leaf Lounge Newsletter powered by
    Mailchimp.

    Methods:
    def test_newsletter_form_email_is_required():
        Asserts the newsletter form is invalid without an email value.
        Asserts the error raised as a result of the empty value stems
        from the "email" key.
        Asserts the error raises matches the expected error.


    def test_newsletter_form_email_format_is_correct():
        Asserts the newsletter form is invalid if the email value is of
        an incorrect format.
        Asserts the error raised as a result of the incorrectly-formatted
        value stems from the "email" key.
        Asserts the error raises matches the expected error.


    def test_correctly_filled_form_is_valid():
        Asserts a correctly filled form is valid.
    """

    def test_newsletter_form_email_is_required(self):
        """
        Asserts the newsletter form is invalid without an email value.
        Asserts the error raised as a result of the empty value stems
        from the "email" key.
        Asserts the error raises matches the expected error.
        """
        newsletter_form = EmailForm({
            "email": ""
        })

        self.assertFalse(newsletter_form.is_valid())
        self.assertIn("email", newsletter_form.errors.keys())
        self.assertEqual(
            newsletter_form.errors["email"][0],
            "This field is required."
        )

    def test_newsletter_form_email_format_is_correct(self):
        """
        Asserts the newsletter form is invalid if the email value is of
        an incorrect format.
        Asserts the error raised as a result of the incorrectly-formatted
        value stems from the "email" key.
        Asserts the error raises matches the expected error.
        """
        newsletter_form = EmailForm({
            "email": "123",
        })

        self.assertFalse(newsletter_form.is_valid())
        self.assertIn("email", newsletter_form.errors.keys())
        self.assertEqual(
            newsletter_form.errors["email"][0],
            "Enter a valid email address."
        )

    def test_correctly_filled_form_is_valid(self):
        newsletter_form = EmailForm({
            "email": "tester@email.com",
        })

        self.assertTrue(newsletter_form.is_valid())
