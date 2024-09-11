from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Signal triggering user_profile creation after user login.
from reader.signals import create_or_save_profile
# Signal triggering community creation after genre save.
from library.signals import create_community_on_genre_save

from library.models import Genre
from .models import *


class TestCommunityModels(TestCase):
    """
    A class for testing models in the Community app.

    Methods:
    def setUp():
        REGISTRATION:
        Simulates user registration to allow for users to access
        community-related functionality and models.

    def test_community_creation():
        Retrieves the appropriate community instance for testing and saves it.
        This process generates the community slug as per the defined format.

        Asserts the community's __str__() returns the expected string for the
        appropriate community instance.

        Asserts the correct community is retrieved.
        Asserts a ValidationError is raised if the community's name is empty.
        Asserts a ValidationError is raised if there is no community name.
        Asserts a ValidationError is raised if the community's name exceeds the
        80 character limit.

        Asserts the community's description matches the model's setup value.

        Asserts the community's slug matches the expected slug string format.
    """
    def setUp(self):
        """
        REGISTRATION:
        Simulates user registration to allow for users to access
        community-related functionality and models.

        GENRE & COMMUNITY:
        Simulates the creation of a genre. After the mock genre
        is saved, a community is automatically created.

        Saves the relevant models to the test sqlite3 database.
        """
        self.client = Client()
        self.user = User(username="ananiko")
        self.user.set_password("modeltesting")
        self.user.save()

        self.genre = Genre(
            name="TestGenre",
            community=None
        )
        self.genre.save()

    def test_community_creation(self):
        """
        Retrieves the appropriate community instance for testing and saves it.
        This process generates the community slug as per the defined format.

        Asserts the community's __str__() returns the expected string for the
        appropriate community instance.

        Asserts the correct community is retrieved.
        Asserts a ValidationError is raised if the community's name is empty.
        Asserts a ValidationError is raised if there is no community name.
        Asserts a ValidationError is raised if the community's name exceeds the
        80 character limit.

        Asserts the community's description matches the model's setup value.

        Asserts the community's slug matches the expected slug string format.
        """
        self.community = self.genre.community
        self.community.save()

        self.assertEqual(self.community.__str__(), "TestGenre Community")

        self.assertEqual(self.community.name, "TestGenre Community")
        with self.assertRaises(ValidationError):
            self.community.name = ""
            self.community.full_clean()
        with self.assertRaises(ValidationError):
            self.community.name = None
            self.community.full_clean()
        with self.assertRaises(ValidationError):
            self.community.name = """zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
            zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
            zzzzzzzzzzzzzzzzz"""
            self.community.full_clean()

        self.assertEqual(
            self.community.description, "Welcome to the TestGenre community!"
        )

        self.assertEqual(
            self.community.slug, f"testgenre-community-{self.community.id}"
        )
