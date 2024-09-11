from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError

# Signal triggering user_profile creation after user login.
from reader.signals import create_or_save_profile
# Signal triggering community creation after genre save.
from .signals import create_community_on_genre_save

from reader.models import UserProfile
from community.models import Community
from .models import *

import datetime


class TestibraryModels(TestCase):
    """
    A class for testing models in the Library app. Testing includes asserting
    equal values to those in the model setup, relational testing (including
    signal triggers) and basic validation.

    Methods:
    def setUp():
        Simulates user log in to allow the creation for workspaces and tasks.
        Simulates the creation of a workspace where workspace.creator field is
        automatically assigned the current User instance.
        Simulates the creation of a task where task.creator is automatically
        assigned the current User instance, and task.workspace is automatically
        assigned the current workspace.

    def test_author_profile_creation_and_validation():
        Asserts the author user profile is the same as the current user's user
        profile.
        Asserts that an author profile can be blank (for authors uploaded via
        admin panel). For registering users, the author profile is created
        automatically.

        Asserts the author's first name matches the model's setup value.
        Asserts a ValidationError is raised if the author's firstname is empty.

        Asserts the author's last name matches the model's setup value.
        Asserts a ValidationError is raised if the author's lastname is empty.

        Asserts the author's d_o_b is a datetime object that matches the
        model's setup value.
        Asserts a ValidationError is raised if the author's d_o_b is of the
        wrong format - this is handled via a date input but just in case.
        Asserts a ValidationError is raised if the author's d_o_b is empty.

        Asserts the author's nationality matches the model's setup value.
        Asserts the author's nationality can be blank.

        Asserts the author's bio matches the model's setup value.
        Asserts a ValidationError is raised if the author's bio is empty.

    def test_genre_and_genre_community_creation():
        Retrieves the appropriate genre instance.
        Asserts the genre's __str__() returns the expected string for the
        appropriate genre instance.

        Asserts the genre name matches the model's setup value.
        Asserts a ValidationError is raised if the genre's name is empty.

        Asserts the genre's community field can be blank.
        Asserts the genre's community's name matches the expected value. A
        community instance is automatically created and linked following a
        new genre creation. This is handled via library.signals.
    """
    def setUp(self):
        """
        REGISTRATION:
        Simulates user registration to allow for the creation of a user profile
        and author profile.

        USER PROFILE & AUTHOR PROFILE:
        Retrieves the user profile automatically created following successful
        user registration. This is handled via
        reader.signals.create_or_save_profile.
        Simulates the creation of an author profile and assigns the relevant
        user profile to the author.user_profile field.

        GENRE & COMMUNITY:
        Simulates the creation of a genre. A community instance associated
        with the genre is created automatically via
        library.signals.create_community_on_genre_save.

        Saves the relevant models to the test sqlite3 database.
        """
        self.client = Client()
        self.user = User(username="ananiko")
        self.user.set_password("modeltesting")
        self.user.save()

        self.user_profile = UserProfile.objects.get(user=self.user)
        self.author = Author(
            user_profile=self.user_profile,
            first_name="Firstname",
            last_name="Lastname",
            d_o_b="1999-01-28",
            nationality="Ireland",
            bio="Test author model bio!"
        )
        self.author.save()

        self.genre = Genre(
            name="TestGenre",
            community=None
        )
        self.genre.save()

    def test_author_profile_creation_and_validation(self):
        """
        Retrieves the appropriate author instance.
        Asserts the author's __str__() returns the expected string for the
        appropriate author instance.

        Asserts the author user profile is the same as the current user's
        user profile.
        Asserts that an author profile can be blank (for authors uploaded via
        admin panel). For registering users, the author profile is created
        automatically. This is handled via reader.signals.

        Asserts the author's first name matches the model's setup value.
        Asserts a ValidationError is raised if the author's firstname is empty.

        Asserts the author's last name matches the model's setup value.
        Asserts a ValidationError is raised if the author's lastname is empty.

        Asserts the author's d_o_b is a datetime object that matches the
        model's setup value.
        Asserts a ValidationError is raised if the author's d_o_b is of the
        wrong format - this is handled via a date input but just in case.
        Asserts a ValidationError is raised if the author's d_o_b is empty.

        Asserts the author's nationality matches the model's setup value.
        Asserts the author's nationality can be blank.

        Asserts the author's bio matches the model's setup value.
        Asserts a ValidationError is raised if the author's bio is empty.
        """
        author = Author.objects.get(user_profile=self.user_profile)
        self.assertEqual(author.__str__(), "Firstname Lastname")

        self.assertEqual(self.author.user_profile, self.user_profile)
        self.assertTrue(self.author.user_profile, "")

        self.assertEqual(self.author.first_name, "Firstname")
        with self.assertRaises(ValidationError):
            self.author.first_name = ""
            self.author.full_clean()

        self.assertEqual(self.author.last_name, "Lastname")
        with self.assertRaises(ValidationError):
            self.author.last_name = ""
            self.author.full_clean()

        self.assertEqual(self.author.d_o_b, datetime.date(1999, 1, 28))
        with self.assertRaises(ValidationError):
            self.author.d_o_b = "28/01/1999"
            self.author.full_clean()
        with self.assertRaises(ValidationError):
            self.author.d_o_b = ""
            self.author.full_clean()

        self.assertEqual(self.author.nationality, "Ireland")
        self.assertTrue(self.author.nationality, "")

        self.assertEqual(self.author.bio, "Test author model bio!")
        with self.assertRaises(ValidationError):
            self.author.bio = ""
            self.author.full_clean()

    def test_genre_and_genre_community_creation(self):
        """
        Retrieves the appropriate genre instance.
        Asserts the genre's __str__() returns the expected string for the
        appropriate genre instance.

        Asserts the genre name matches the model's setup value.
        Asserts a ValidationError is raised if the genre's name is empty.

        Asserts the genre's community field can be blank.
        Asserts the genre's community's name matches the expected value. A
        community instance is automatically created and linked following a
        new genre creation. This is handled via library.signals.
        """
        genre = Genre.objects.get(name="TestGenre")
        self.assertEqual(genre.__str__(), "TestGenre")

        self.assertEqual(self.genre.name, "TestGenre")
        with self.assertRaises(ValidationError):
            self.genre.name = ""
            self.genre.full_clean()

        self.assertTrue(self.genre.community, "")
        self.assertEqual(self.genre.community.name, "TestGenre Community")
