from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decimal import Decimal

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

        BOOK:
        Simulates the creation of a book with relevant relationships to the
        author and genre models.

        REVIEW:
        Simulates the creation of a review with relevant relationships to the
        user_profile and book models.

        Saves the relevant models to the test sqlite3 database.


    def test_author_profile_creation_and_validation():
        Retrieves the appropriate author instance for testing.
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
        Retrieves the appropriate genre instance for testing.
        Asserts the genre's __str__() returns the expected string for the
        appropriate genre instance.

        Asserts the genre name matches the model's setup value.
        Asserts a ValidationError is raised if the genre's name is empty.

        Asserts the genre's community field can be blank.
        Asserts the genre's community's name matches the expected value. A
        community instance is automatically created and linked following a
        new genre creation. This is handled via library.signals.


    def test_book_creation():
        Retrieves the appropriate book instance for testing.
        Asserts the book's __str__() returns the expected string for the
        appropriate book instance.

        Asserts the book name matches the model's setup value.
        Asserts a ValidationError is raised if the book's name is empty.
        Asserts a ValidationError is raised if the book's name is longer
        than 100 characters.

        Asserts the book isbn matches the model's setup value.
        Asserts a ValidationError is raised if the book's isbn is empty.
        Asserts a ValidationError is raised if the book's isbn is longer
        than 13 characters.

        Asserts a slug is automatically generated after a book instance is
        saved.

        Asserts the book author's firstname matches the model's setup value.
        Asserts a ValidationError is raised if there is no author.

        Asserts the book genre matches the model's setup value.
        Asserts a ValidationError is raised if there is no genre.

        Asserts the book blurb matches the model's setup value.
        Asserts a ValidationError is raised if the book's blurb is empty.

        Asserts the book's year_published field matches the model's setup
        value.
        Asserts a ValidationError is raised if the book's year_published is
        of the wrong format.
        Asserts a ValidationError is raised if the book's year_published is
        empty.
        Asserts a ValidationError is raised if there is no year_published
        value.

        Asserts the book publisher matches the model's setup value.
        Asserts the book publisher can be empty.

        Asserts the book cover-type matches the model's setup value.
        Asserts a ValidationError is raised if there is no cover-type value.
        Asserts a ValidationError is raised if the book's cover-type is empty.

        Asserts the book's date_added field value is a datetime object that
        matches the model's setup value.
        Asserts a ValidationError is raised if there is no date_added value.
        Asserts a ValidationError is raised if the book's date_added is empty.
        Asserts a ValidationError is raised if the book's date_added is of the
        wrong format.

        Asserts the book's price field is a Decimal format that matches the
        model's setup value.
        Asserts a ValidationError is raised if the book's price is empty.
        Asserts a ValidationError is raised if the book's price is over 5
        decimals, i.e., a book's value is raised too high.


    def test_review_creation():
        Retrieves the appropriate review instance for testing.
        Asserts the review's __str__() returns the expected string for the
        appropriate review instance.

        Asserts the reviewer is the user profile as per model setup.
        Asserts the user profile belongs to the user as per model setup.
        Asserts a ValidationError is raised if a review is without a reviewer.

        Asserts the book reviewed matches the model's setup value.
        Asserts a ValidationError is raised if there is no book title (no book)
        associated with the review.

        Asserts the review title matches the model's setup value.
        Asserts a ValidationError is raised if the review title is empty.
        Asserts a ValidationError is raised if the review title is over the 80
        character limit as defined in models.py.

        Asserts the review rating matches the model's setup value.
        Asserts a ValidationError is raised if there is no review rating.
        Asserts a ValidationError is raised if the rating is over 10.
        Asserts a ValidationError is raised if the rating is below 0.

        Asserts the review comment matches the model's setup value.
        Asserts a ValidationError is raised if there is no comment.

        Asserts today's (11-09-2024) date is automatically saved to
        the review's reviewed_on field.
        Asserts a validation error is raised if the reviewed_on date
        is missing.

        Asserts the newly saved review is saved as an unapproved instance.
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

        BOOK:
        Simulates the creation of a book with relevant relationships to the
        author and genre models.

        REVIEW:
        Simulates the creation of a review with relevant relationships to the
        user_profile and book models.

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

        self.book = Book(
            title="How to Test Django Models",
            isbn="0-061-96436-0",
            slug=None,
            author=self.author,
            genre=self.genre,
            blurb="Test Test Test Test Test",
            year_published=1999,
            publisher="Test Publisher",
            type="Softcover",
            date_added="2024-09-11",
            price=14.99
        )
        self.book.save()

        self.review = Review(
            reviewer=self.user_profile,
            book=self.book,
            title="Test Review Title",
            rating=8,
            comment="Test review content body",
        )
        self.review.save()

    def test_author_profile_creation_and_validation(self):
        """
        Retrieves the appropriate author instance for testing.
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
        Retrieves the appropriate genre instance for testing.
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

        self.assertEqual(genre.name, "TestGenre")
        with self.assertRaises(ValidationError):
            self.genre.name = ""
            self.genre.full_clean()

        self.assertTrue(self.genre.community, "")
        self.assertEqual(self.genre.community.name, "TestGenre Community")

    def test_book_creation(self):
        """
        Retrieves the appropriate book instance for testing.
        Asserts the book's __str__() returns the expected string for the
        appropriate book instance.

        Asserts the book name matches the model's setup value.
        Asserts a ValidationError is raised if the book's name is empty.
        Asserts a ValidationError is raised if the book's name is longer
        than 100 characters.

        Asserts the book isbn matches the model's setup value.
        Asserts a ValidationError is raised if the book's isbn is empty.
        Asserts a ValidationError is raised if the book's isbn is longer
        than 13 characters.

        Asserts a slug is automatically generated after a book instance is
        saved.

        Asserts the book author's firstname matches the model's setup value.
        Asserts a ValidationError is raised if there is no author.

        Asserts the book genre matches the model's setup value.
        Asserts a ValidationError is raised if there is no genre.

        Asserts the book blurb matches the model's setup value.
        Asserts a ValidationError is raised if the book's blurb is empty.

        Asserts the book's year_published field matches the model's setup
        value.
        Asserts a ValidationError is raised if the book's year_published is
        of the wrong format.
        Asserts a ValidationError is raised if the book's year_published is
        empty.
        Asserts a ValidationError is raised if there is no year_published
        value.

        Asserts the book publisher matches the model's setup value.
        Asserts the book publisher can be empty.

        Asserts the book cover-type matches the model's setup value.
        Asserts a ValidationError is raised if there is no cover-type value.
        Asserts a ValidationError is raised if the book's cover-type is empty.

        Asserts the book's date_added field value is a datetime object that
        matches the model's setup value.
        Asserts a ValidationError is raised if there is no date_added value.
        Asserts a ValidationError is raised if the book's date_added is empty.
        Asserts a ValidationError is raised if the book's date_added is of the
        wrong format.

        Asserts the book's price field is a Decimal format that matches the
        model's setup value.
        Asserts a ValidationError is raised if the book's price is empty.
        Asserts a ValidationError is raised if the book's price is over 5
        decimals, i.e., a book's value is raised too high.
        """
        book = Book.objects.get(author=self.author, genre=self.genre)
        self.assertEqual(
            book.__str__(),
            '"How to Test Django Models" by Firstname Lastname'
        )

        self.assertEqual(book.title, "How to Test Django Models")
        with self.assertRaises(ValidationError):
            self.book.title = ""
            self.book.full_clean()
        with self.assertRaises(ValidationError):
            self.book.title = """zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
            zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
            zzzzzzzzzzzzzzzzz"""
            self.book.full_clean()

        self.assertEqual(book.isbn, "0-061-96436-0")
        with self.assertRaises(ValidationError):
            self.book.isbn = ""
            self.book.full_clean()
        with self.assertRaises(ValidationError):
            self.book.isbn = "ISBN0-061-96436-0"
            self.book.full_clean()

        self.assertEqual(book.slug, "how-to-test-django-models-lastname")

        self.assertEqual(book.author.first_name, "Firstname")
        with self.assertRaises(ValidationError):
            self.book.author = None
            self.book.full_clean()

        self.assertEqual(book.genre.name, "TestGenre")
        with self.assertRaises(ValidationError):
            self.book.genre = None
            self.book.full_clean()

        self.assertEqual(book.blurb, "Test Test Test Test Test")
        with self.assertRaises(ValidationError):
            self.book.blurb = ""
            self.book.full_clean()

        self.assertEqual(book.year_published, 1999)
        with self.assertRaises(ValidationError):
            self.book.year_published = None
            self.book.full_clean()
        with self.assertRaises(ValidationError):
            self.book.year_published = ""
            self.book.full_clean()

        self.assertEqual(book.publisher, "Test Publisher")
        self.assertTrue(book.publisher, "")

        self.assertEqual(book.type, "Softcover")
        with self.assertRaises(ValidationError):
            self.book.type = None
            self.book.full_clean()
        with self.assertRaises(ValidationError):
            self.book.type = ""
            self.book.full_clean()

        self.assertEqual(book.date_added, datetime.date.today())
        with self.assertRaises(ValidationError):
            self.book.date_added = None
            self.book.full_clean()
        with self.assertRaises(ValidationError):
            self.book.date_added = ""
            self.book.full_clean()
        with self.assertRaises(ValidationError):
            self.book.date_added = "11/09/2024"
            self.book.full_clean()

        self.assertEqual(book.price, Decimal('14.99'))
        with self.assertRaises(ValidationError):
            self.book.price = ""
            self.book.full_clean()
        with self.assertRaises(ValidationError):
            self.book.price = Decimal('1409.99')
            self.book.full_clean()

    def test_review_creation(self):
        """
        Retrieves the appropriate review instance for testing.
        Asserts the review's __str__() returns the expected string for the
        appropriate review instance.

        Asserts the reviewer is the user profile as per model setup.
        Asserts the user profile belongs to the user as per model setup.
        Asserts a ValidationError is raised if a review is without a reviewer.

        Asserts the book reviewed matches the model's setup value.
        Asserts a ValidationError is raised if there is no book title (no book)
        associated with the review.

        Asserts the review title matches the model's setup value.
        Asserts a ValidationError is raised if the review title is empty.
        Asserts a ValidationError is raised if the review title is over the 80
        character limit as defined in models.py.

        Asserts the review rating matches the model's setup value.
        Asserts a ValidationError is raised if there is no review rating.
        Asserts a ValidationError is raised if the rating is over 10.
        Asserts a ValidationError is raised if the rating is below 0.

        Asserts the review comment matches the model's setup value.
        Asserts a ValidationError is raised if there is no comment.

        Asserts today's (11-09-2024) date is automatically saved to
        the review's reviewed_on field.
        Asserts a validation error is raised if the reviewed_on date
        is missing.

        Asserts the newly saved review is saved as an unapproved instance.
        """
        review = Review.objects.get(reviewer=self.user_profile, book=self.book)
        # Line breaks PEP8 standards but no way of shortening.
        self.assertEqual(
            review.__str__(),
            'Review for "How to Test Django Models" by Firstname Lastname : 8/10'
        )

        self.assertEqual(review.reviewer, self.user_profile)
        self.assertEqual(review.reviewer.user, self.user)
        with self.assertRaises(ValidationError):
            self.review.reviewer = None
            self.review.full_clean()

        self.assertEqual(review.book.title, "How to Test Django Models")
        with self.assertRaises(ValidationError):
            self.review.book.title = ""
            self.review.full_clean()

        self.assertEqual(review.title, "Test Review Title")
        with self.assertRaises(ValidationError):
            self.review.book.title = ""
            self.review.full_clean()
        with self.assertRaises(ValidationError):
            self.review.book.title = """zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
            zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
            zzzzzzzzzzzzzzzzz"""
            self.review.full_clean()

        self.assertEqual(review.rating, 8)
        with self.assertRaises(ValidationError):
            self.review.rating = None
            self.review.full_clean()
        with self.assertRaises(ValidationError):
            self.review.rating = 15
            self.review.full_clean()
        with self.assertRaises(ValidationError):
            self.review.rating = -2
            self.review.full_clean()

        self.assertEqual(review.comment, "Test review content body")
        with self.assertRaises(ValidationError):
            self.review.comment = None
            self.review.full_clean()

        # Tested on 11/09/2024.
        self.assertEqual(review.reviewed_on, datetime.date.today())
        with self.assertRaises(ValidationError):
            self.review.reviewed_on = None
            self.review.full_clean()

        self.assertEqual(review.approved, False)
