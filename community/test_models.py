from django.shortcuts import get_object_or_404
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils import timezone

# Signal triggering user_profile creation after user login.
from reader.signals import create_or_save_profile
# Signal triggering community creation after genre save.
from library.signals import create_community_on_genre_save

from library.models import Genre
from .models import *

import datetime


class TestCommunityModel(TestCase):
    """
    A class for testing the community model. Testing includes asserting
    equal values to those in the model setup, save method testing, and
    format validation for datetime objects and slugs.

    Methods:
    def setUp():
        REGISTRATION:
        Simulates user registration to allow for users to access
        community-related functionality and models.

        GENRE & COMMUNITY:
        Simulates the creation of a genre. After the mock genre
        is saved, a community is automatically created.

        Saves the relevant models to the test sqlite3 database.


    def test_community_creation_following_genre_creation():
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
        Asserts a ValidationError is thrown if the slug is inputted or
        generated in an incorrect format.
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

    def test_community_creation_following_genre_creation(self):
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
        Asserts a ValidationError is thrown if the slug is inputted or
        generated in an incorrect format.
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
        with self.assertRaises(ValidationError):
            self.community.slug = "incorrectformat"
            self.community.full_clean()


class TestForumAndMessageModels(TestCase):
    """
    A class for testing the forum and message models in the Community app.
    Testing includes asserting equal values to those in the model setup,
    save method testing, user profile association, and format validation
    for datetime objects and slugs.

    Methods:
    def setUp()
        REGISTRATION:
        Simulates user registration to allow for the creation of a user
        profile.

        USER PROFILE & AUTHOR PROFILE:
        Retrieves the user profile automatically created following successful
        user registration. This is handled via
        reader.signals.create_or_save_profile.

        GENRE & COMMUNITY & FORUM:
        Simulates the creation of a genre. After the mock genre
        is saved, a community is automatically created. After
        the community is saved, forums can be created inside the
        community.
        Simulates the creation of a forum and saves it.

        MESSAGE:
        Simulates the creation of a message and saves it.

        Saves the relevant models to the test sqlite3 database.


    def test_forum_creation():
        Retrieves the appropriate forum instance for testing.
        Asserts the forum's __str__() returns the expected string for the
        appropriate forum instance.

        Asserts the correct forum is retrieved by checking the name.
        Asserts a ValidationError is raised if the forum's name is empty.
        Asserts a ValidationError is raised if there is no forum name.
        Asserts a ValidationError is raised if the forum's name exceeds the
        80 character limit.

        Asserts the forum slug is automatically generated in the correct
        format after the instance is saved.
        Asserts a ValidationError is thrown if the slug is inputted or
        generated in an incorrect format.

        Asserts the forum's date_added matches today's date.
        Asserts a ValidationError is thrown if the date_added is does not match
        today's date.

        Asserts the forum is created inside the correct community by checking
        the name of the community.


    def test_message_creation():
        Retrieves the appropriate message instance for testing.
        Asserts the message's __str__() returns the expected string for the
        appropriate message instance.

        Asserts the message is created inside the correct forum by checking
        its associated forum name.

        Asserts the message's content matches the model's setup value.
        Asserts a ValidationError is raised if the message's content is empty.
        Asserts a ValidationError is raised if there is no message content.

        Asserts the message sender matches the expected user profile.
        Asserts the message sender's username matches the expected value.

        Asserts the message's date_sent matches today's date.
        Asserts a ValidationError is thrown if the date_sent does not match
        today's date.
    """
    def setUp(self):
        """
        REGISTRATION:
        Simulates user registration to allow for the creation of a user
        profile.

        USER PROFILE & AUTHOR PROFILE:
        Retrieves the user profile automatically created following successful
        user registration. This is handled via
        reader.signals.create_or_save_profile.

        GENRE & COMMUNITY & FORUM:
        Simulates the creation of a genre. After the mock genre
        is saved, a community is automatically created. After
        the community is saved, forums can be created inside the
        community.
        Simulates the creation of a forum and saves it.

        MESSAGE:
        Simulates the creation of a message and saves it.

        Saves the relevant models to the test sqlite3 database.
        """
        self.client = Client()
        self.user = User(username="ananiko")
        self.user.set_password("modeltesting")
        self.user.save()

        self.user_profile = get_object_or_404(UserProfile, user=self.user)

        self.genre = Genre(
            name="TestGenre",
            community=None
        )
        self.genre.save()

        self.community = self.genre.community
        self.community.save()

        self.forum = Forum(
            name="Test Forum",
            community=self.community
        )
        self.forum.save()

        self.message = Message(
            forum=self.forum,
            content="test message",
            messenger=self.user_profile,
            date_sent=timezone.now()
        )
        self.message.save()

    def test_forum_creation(self):
        """
        Retrieves the appropriate forum instance for testing.
        Asserts the forum's __str__() returns the expected string for the
        appropriate forum instance.

        Asserts the correct forum is retrieved by checking the name.
        Asserts a ValidationError is raised if the forum's name is empty.
        Asserts a ValidationError is raised if there is no forum name.
        Asserts a ValidationError is raised if the forum's name exceeds the
        80 character limit.

        Asserts the forum slug is automatically generated in the correct
        format after the instance is saved.
        Asserts a ValidationError is thrown if the slug is inputted or
        generated in an incorrect format.

        Asserts the forum's date_added matches today's date.
        Asserts a ValidationError is thrown if the date_added does not match
        today's date.

        Asserts the forum is created inside the correct community by checking
        the name of the community.
        """
        forum = get_object_or_404(Forum, community=self.community)
        self.assertEqual(forum.__str__(), f"{forum.name}")

        self.assertEqual(forum.name, "Test Forum")
        with self.assertRaises(ValidationError):
            self.forum.name = ""
            self.forum.full_clean()
        with self.assertRaises(ValidationError):
            self.forum.name = None
            self.forum.full_clean()
        with self.assertRaises(ValidationError):
            self.forum.name = """zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
            zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
            zzzzzzzzzzzzzzzzz"""
            self.forum.full_clean()

        self.assertEqual(forum.slug, f"test-forum-" + slugify(
            f"{self.community.name}") + f"-{self.forum.id}"
        )
        with self.assertRaises(ValidationError):
            self.forum.slug = "incorrectformat"
            self.forum.full_clean()

        self.assertEqual(forum.date_created, timezone.now().date())
        with self.assertRaises(ValidationError):
            self.forum.date_created = timezone.now()
            self.forum.full_clean()

        self.assertEqual(forum.community.name, "TestGenre Community")

    def test_message_creation(self):
        """
        Retrieves the appropriate message instance for testing.
        Asserts the message's __str__() returns the expected string for the
        appropriate message instance.

        Asserts the message is created inside the correct forum by checking
        its associated forum name.

        Asserts the message's content matches the model's setup value.
        Asserts a ValidationError is raised if the message's content is empty.
        Asserts a ValidationError is raised if there is no message content.

        Asserts the message sender matches the expected user profile.
        Asserts the message sender's username matches the expected value.

        Asserts the message's date_sent matches today's date.
        Asserts a ValidationError is thrown if the date_sent does not match
        today's date.
        """
        self.message = get_object_or_404(Message, messenger=self.user_profile)
        self.assertEqual(
            self.message.__str__(), f"Message in '{self.message.forum.name}'"
        )

        self.assertEqual(self.message.forum.name, f"Test Forum")

        self.assertEqual(self.message.content, "test message")
        with self.assertRaises(ValidationError):
            self.message.content = ""
            self.message.full_clean()
        with self.assertRaises(ValidationError):
            self.message.content = None
            self.message.full_clean()

        self.assertEqual(self.message.messenger, self.user_profile)
        self.assertEqual(self.message.messenger.user.username, "ananiko")

        self.assertEqual(self.message.date_sent.date(), timezone.now().date())
        with self.assertRaises(ValidationError):
            self.message.date_sent = timezone.now().date()
            self.message.full_clean()
