from django.test import TestCase
from django.urls import reverse, resolve
from .views import *


class TestCheckoutURLs(TestCase):
    """
    A class for testing URLs associated with the checkout app.
    This class tests urls resolve from their FBVs.

    Methods:
    def test_checkout_resolves():
        Reverses the URL name and checks if it returns the correct FBV of
        checkout.

        Asserts the checkout view (checkout) is resolved from 'checkout'.


    def test_success_resolves():
        Reverses the URL name with arguments [str:order_number] and checks if it
        returns the correct FBV of success.

        Asserts the view called after successful checkout (success) is resolved
        from 'success' with a str argument of the order number.
    """

    def test_checkout_resolves(self):
        """
        Asserts the checkout view (checkout) is resolved from 'checkout'.
        """
        path = reverse('checkout')
        self.assertEqual(resolve(path).func, checkout)

    def test_success_resolves(self):
        """
        Asserts the view called after successful checkout (success) is resolved
        from 'success' with a str argument of the order number.
        """
        path = reverse('success', args=['2ED525BC578441068612D5EDAFC6FBEE'])
        self.assertEqual(resolve(path).func, success)
