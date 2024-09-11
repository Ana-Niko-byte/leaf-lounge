from django.test import TestCase, Client
from django.contrib.auth.models import User

# Signal triggering user_profile creation after user login.
from reader.signals import create_or_save_profile

from .models import *


class TestCommunityModels(TestCase):
    """
    A class for testing models in the Community app.

    Methods:
    def setUp():
        REGISTRATION:
        Simulates user registration to allow for users to access
        community-related functionality and models.
    """
    def setUp(self):
        """
        REGISTRATION:
        Simulates user registration to allow for users to access
        community-related functionality and models.
        """
        self.client = Client()
        self.user = User(username="ananiko")
        self.user.set_password("modeltesting")
        self.user.save()

    