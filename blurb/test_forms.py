from django.test import TestCase
from .forms import *


class TestContactForm(TestCase):
    """
    A class for testing the Contact Form associated with the Blurb app.
    This form allows users to contact the Leaf Lounge team with queries.

    Methods:
    def test_contact_for_name_is_required():
        Asserts the contact form is invalid without a name value.
        Asserts the error raised as a result of the empty value stems
        from the "name" key.
        Asserts the error raises matches the expected error.


    def test_contact_form_email_is_required():
        Asserts the contact form is invalid without an email value.
        Asserts the error raised as a result of the empty value stems
        from the "email" key.
        Asserts the error raises matches the expected error.


    def test_contact_form_email_format_is_correct():
        Asserts the contact form is invalid if the email value is of
        an incorrect format.
        Asserts the error raised as a result of the incorrectly-formatted
        value stems from the "email" key.
        Asserts the error raises matches the expected error.

    def test_contact_form_subject_is_required():
        Asserts the contact form is invalid without a subject value.
        Asserts the error raised as a result of the empty value stems
        from the "subject" key.
        Asserts the error raises matches the expected error.


    def test_contact_form_message_is_required():
        Asserts the contact form is invalid without a message value.
        Asserts the error raised as a result of the empty value stems
        from the "message" key.
        Asserts the error raises matches the expected error.


    def test_correctly_filled_form_is_valid():
        Asserts a correctly filled form is valid.
    """
    def test_contact_for_name_is_required(self):
        """
        Asserts the contact form is invalid without a name value.
        Asserts the error raised as a result of the empty value stems
        from the "name" key.
        Asserts the error raises matches the expected error.
        """
        contact_form = ContactForm({
            "name": "",
            "email": "tester@email.com",
            "subject": "Career Opportunities",
            "message": "Testing the form."
        })
        
        self.assertFalse(contact_form.is_valid())
        self.assertIn("name", contact_form.errors.keys())
        self.assertEqual(
            contact_form.errors["name"][0],
            "This field is required."
        )

    def test_contact_form_email_is_required(self):
        """
        Asserts the contact form is invalid without an email value.
        Asserts the error raised as a result of the empty value stems
        from the "email" key.
        Asserts the error raises matches the expected error.
        """
        contact_form = ContactForm({
            "name": "Tester",
            "email": "",
            "subject": "Career Opportunities",
            "message": "Testing the form."
        })
        
        self.assertFalse(contact_form.is_valid())
        self.assertIn("email", contact_form.errors.keys())
        self.assertEqual(
            contact_form.errors["email"][0],
            "This field is required."
        )

    def test_contact_form_email_format_is_correct(self):
        """
        Asserts the contact form is invalid if the email value is of
        an incorrect format.
        Asserts the error raised as a result of the incorrectly-formatted
        value stems from the "email" key.
        Asserts the error raises matches the expected error.
        """
        contact_form = ContactForm({
            "name": "Tester",
            "email": "123",
            "subject": "Career Opportunities",
            "message": "Testing the form."
        })
        
        self.assertFalse(contact_form.is_valid())
        self.assertIn("email", contact_form.errors.keys())
        self.assertEqual(
            contact_form.errors["email"][0],
            "Enter a valid email address."
        )

    def test_contact_form_subject_is_required(self):
        """
        Asserts the contact form is invalid without a subject value.
        Asserts the error raised as a result of the empty value stems
        from the "subject" key.
        Asserts the error raises matches the expected error.
        """
        contact_form = ContactForm({
            "name": "Tester",
            "email": "tester@email.com",
            "subject": "",
            "message": "Testing the form."
        })
        
        self.assertFalse(contact_form.is_valid())
        self.assertIn("subject", contact_form.errors.keys())
        self.assertEqual(
            contact_form.errors["subject"][0],
            "This field is required."
        )

    def test_contact_form_message_is_required(self):
        """
        Asserts the contact form is invalid without a message value.
        Asserts the error raised as a result of the empty value stems
        from the "message" key.
        Asserts the error raises matches the expected error.
        """
        contact_form = ContactForm({
            "name": "Tester",
            "email": "tester@email.com",
            "subject": "Career Opportunities",
            "message": ""
        })
        
        self.assertFalse(contact_form.is_valid())
        self.assertIn("message", contact_form.errors.keys())
        self.assertEqual(
            contact_form.errors["message"][0],
            "This field is required."
        )

    def test_correctly_filled_form_is_valid(self):
        """
        Asserts a correctly filled form is valid.
        """
        contact_form = ContactForm({
            "name": "Tester",
            "email": "tester@email.com",
            "subject": "Career Opportunities",
            "message": "Testing this form."
        })
        
        self.assertTrue(contact_form.is_valid())
