from django.test import TestCase
from django.urls import reverse, resolve
from .views import *


class TestMarketingURLs(TestCase):
    """
    A class for testing URLs associated with the marketing app.
    This class tests urls resolve from their FBVs.

    Methods:
    def test_subscribe_resolves():
        Reverses the URL name and checks if it returns the correct FBV of
        subscribe.

        Asserts the newsletter subscribe view (subscribe_view) resolves from
        'subscribe'.


    def test_unsubscribe_resolves():
        Reverses the URL name and checks if it returns the correct FBV of
        unsubscribe.

        Asserts the newsletter unsubscribe view (unsubscribe_view) resolves
        from 'unsubscribe'.
    """

    def test_subscribe_resolves(self):
        """
        Asserts the newsletter subscribe view (subscribe_view) resolves
        from 'subscribe'.
        """
        path = reverse('subscribe')
        self.assertEqual(resolve(path).func, subscribe_view)

    def test_unsubscribe_resolves(self):
        """
        Asserts the newsletter unsubscribe view (unsubscribe_view) resolves
        from 'unsubscribe'.
        """
        path = reverse('unsubscribe')
        self.assertEqual(resolve(path).func, unsubscribe_view)
