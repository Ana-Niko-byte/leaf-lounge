from django.test import TestCase
from django.urls import reverse, resolve
from .views import *


class TestBlurbURLs(TestCase):
    '''
    A class for testing URLs associated with the blurb app.

    Methods:
    def test_home_resolves():
        Reverses the URL name and checks the correct FBV of blurb returns.
        Asserts the home view (blurb) is resolved from 'home'.

    def test_contact_resolves():
        Reverses the URL name and checks the correct FBV of contact returns.
        Asserts the contact view (contact) is resolved from 'contact'.
    '''
    def test_home_resolves(self):
        '''
        Asserts the home view (blurb) is resolved from 'home'.
        '''
        path = reverse('home')
        self.assertEqual(resolve(path).func, blurb)

    def test_contact_resolves(self):
        '''
        Asserts the contact view (contact) is resolved from 'contact'.
        '''
        path = reverse('contact')
        self.assertEqual(resolve(path).func, contact)
