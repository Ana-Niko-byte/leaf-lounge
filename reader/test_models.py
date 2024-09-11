from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError

# Signal triggering user_profile creation after user login.
from .signals import create_or_save_profile

from .models import *


class TestUserProfile(TestCase):
    """
    A class for testing models in the Reader app. Testing includes asserting
    a user profile is successfully created following user registration, and
    that the created user profile belongs to the registered user.

    Methods:
    def setUp():
        REGISTRATION:
        Simulates user registration to allow for the creation of a user
        profile.


    def test_user_profile_creation_on_user_registration():
        Retrieves the appropriate user profile instance for testing.
        Asserts a user profile is successfully created following
        user registration.
        Asserts the user profile's __str__() returns the expected string for
        the appropriate user profile instance.
    """
    def setUp(self):
        """
        REGISTRATION:
        Simulates user registration to allow for the creation of a user
        profile.
        """
        self.client = Client()
        self.user = User(username="ananiko")
        self.user.set_password("modeltesting")
        self.user.save()

    def test_user_profile_creation_on_user_registration(self):
        """
        Retrieves the appropriate user profile instance for testing.
        Asserts a user profile is successfully created following
        user registration.
        Asserts the user profile's __str__() returns the expected string for
        the appropriate user profile instance.
        """
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(user_profile.user.username, "ananiko")
        self.assertEqual(user_profile.__str__(), "ananiko")
