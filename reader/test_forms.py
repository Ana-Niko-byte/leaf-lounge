from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from library.models import *
from .forms import *


class TestUserProfileForm(TestCase):
    """
    A class for testing the UserProfile Form associated with the reader app.
    This form allows users to streamline the checkout process by pre-filling
    their information on the checkout page.

    Methods:
    def test_user_profile_form_information_is_not_required():
        Asserts the user profile form is valid even if there is no information
        provided. These fields are optional.


    def test_fully_and_correctly_filled_form_is_valid():
        Asserts the user profile form is valid with all information provided.
        These fields are optional, but are used for faster checkout processes.


    def test_partially_but_correctly_filled_form_is_valid():
        Asserts the user profile form is valid with partial information
        provided.
        These fields are optional, but are used for faster checkout processes.
    """
    def test_user_profile_form_information_is_not_required(self):
        """
        Asserts the user profile form is valid even if there is no information
        provided. These fields are optional.
        """
        user_profile_form = UserProfileForm({
            "full_name": "",
            "email": "",
            "phone_number": "",
            "street_1": "",
            "street_2": "",
            "town_city": "",
            "postcode": "",
            "county": "",
            "country": ""
        })
        self.assertTrue(user_profile_form.is_valid())

    def test_fully_and_correctly_filled_form_is_valid(self):
        """
        Asserts the user profile form is valid with all information provided.
        These fields are optional, but are used for faster checkout processes.
        """
        user_profile_form = UserProfileForm({
            "full_name": "Tester Tester",
            "email": "tester@email.com",
            "phone_number": "123 456 7890",
            "street_1": "Street Address 1",
            "street_2": "Street Address 2",
            "town_city": "Town",
            "postcode": "12345",
            "county": "County",
            "country": "IE"
        })
        self.assertTrue(user_profile_form.is_valid())

    def test_partially_but_correctly_filled_form_is_valid(self):
        """
        Asserts the user profile form is valid with partial information
        provided.
        These fields are optional, but are used for faster checkout processes.
        """
        user_profile_form = UserProfileForm({
            "full_name": "Tester Tester",
            "email": "tester@email.com",
            "phone_number": "123 456 7890",
            "street_1": "Street Address 1",
            "street_2": "",
            "town_city": "Town",
            "postcode": "",
            "county": "",
            "country": "IE"
        })
        self.assertTrue(user_profile_form.is_valid())


class TestReviewForm(TestCase):
    """
    A class for testing the Review Form associated with the reader app.
    This form allows users leave reviews on books they have purchased. This
    form can be accessed through "My Books" > "Leave a Review", and all pending
    and approved reviews can be viewed under "My Profile" > "My Reviews".

    Methods:
    def setUp():
        REGISTRATION:
        Simulates user registration to allow for the creation of a user
        profile.

        USER PROFILE & AUTHOR PROFILE:
        Retrieves the user profile automatically created following successful
        user registration. This is handled via
        reader.signals.create_or_save_profile.
        Simulates the creation of an author profile and assigns the relevant
        user profile to the author.user_profile field.

        GENRE & COMMUNITY:
        Simulates the creation of a genre.

        BOOK:
        Simulates the creation of a book with relevant relationships to the
        author and genre models. This is required as reviews need a valid book
        instance.

        Saves the relevant models to the test sqlite3 database.
        Retrieves the relevant URLs and assigns them to variables for testing.


    def test_review_form_book_is_required():
        Asserts the review form is invalid with an empty book value.
        Asserts the error raised as a result of the incorrect value stems
        from the "book" key.
        Asserts the error raises matches the expected error.


    def test_review_form_book_must_be_valid():
        Asserts the review form is invalid with an incorrect book value.
        This means a value that does not reference a book in the database.
        Asserts the error raised as a result of the incorrect value stems
        from the "book" key.
        Asserts the error raises matches the expected error.


    def test_review_form_title_is_required():
        Asserts the review form is invalid with an empty title value.
        Asserts the error raised as a result of the incorrect value stems
        from the "title" key.
        Asserts the error raises matches the expected error.


    def test_review_form_rating_is_required():
        Asserts the review form is invalid with an empty rating value.
        Asserts the error raised as a result of the incorrect value stems
        from the "rating" key.
        Asserts the error raises matches the expected error.


    def test_review_form_rating_must_be_more_than__or_equal_1():
        Asserts the review form is invalid with a rating value <1.
        Asserts the error raised as a result of the incorrect value stems
        from the "rating" key.
        Asserts the error raises matches the expected error.


    def test_review_form_rating_must_be_less_than_or_equal_10():
        Asserts the review form is invalid with a rating value >10.
        Asserts the error raised as a result of the incorrect value stems
        from the "rating" key.
        Asserts the error raises matches the expected error.


    def test_review_form_comment_is_required():
        Asserts the review form is invalid with an empty comment value.
        Asserts the error raised as a result of the incorrect value stems
        from the "comment" key.
        Asserts the error raises matches the expected error.


    def test_review_form_is_valid():
        Asserts a review form instance that is full and correctly filled
        out is valid.
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
            Simulates the creation of an author profile and assigns the relevant
            user profile to the author.user_profile field.

        GENRE & COMMUNITY:
        Simulates the    creation of a genre.

        BOOK:
            Simulates the creation of a book with relevant relationships to the
            author and genre models. This is required as reviews need a valid book
            instance.

        Saves the relevant models to the test sqlite3 database.
        Retrieves the relevant URLs and assigns them to variables for testing.
        """
        self.client = Client()
        self.user = User(username="ananiko")
        self.user.set_password("viewtesting")
        self.user.save()
        self.Client = Client()

        self.client.login(
            username="ananiko",
            password="viewtesting"
        )

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

        placeholder_image = SimpleUploadedFile(
            name="bookplaceholder.png",
            content=b"",
            content_type="image/png"
        )

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
            price=14.99,
            image=placeholder_image
        )
        self.book.save()

    def test_review_form_book_is_required(self):
        """
        Asserts the review form is invalid with an empty book value.
        Asserts the error raised as a result of the incorrect value stems
        from the "book" key.
        Asserts the error raises matches the expected error.
        """
        review_form = ReviewForm({
            "book": "",
            "title": "Test Title",
            "rating": 4,
            "comment": "Not bad"
        })
        self.assertFalse(review_form.is_valid())

    def test_review_form_book_must_be_valid(self):
        """
        Asserts the review form is invalid with an incorrect book value.
        This means a value that does not reference a book in the database.
        Asserts the error raised as a result of the incorrect value stems
        from the "book" key.
        Asserts the error raises matches the expected error.
        """
        review_form = ReviewForm({
            "book": "Not a Valid Book",
            "title": "Test Title",
            "rating": 4,
            "comment": "Not bad"
        })
        self.assertFalse(review_form.is_valid())
        self.assertIn("book", review_form.errors.keys())

    def test_review_form_title_is_required(self):
        """
        Asserts the review form is invalid with an empty title value.
        Asserts the error raised as a result of the incorrect value stems
        from the "title" key.
        Asserts the error raises matches the expected error.
        """
        review_form = ReviewForm({
            "book": self.book,
            "title": "",
            "rating": 4,
            "comment": "Not bad"
        })
        self.assertFalse(review_form.is_valid())
        self.assertIn("title", review_form.errors.keys())
        self.assertEqual(
            review_form.errors["title"][0],
            "This field is required."
        )

    def test_review_form_rating_is_required(self):
        """
        Asserts the review form is invalid with an empty rating value.
        Asserts the error raised as a result of the incorrect value stems
        from the "rating" key.
        Asserts the error raises matches the expected error.
        """
        review_form = ReviewForm({
            "book": self.book,
            "title": "Test Title",
            "rating": "",
            "comment": "Not bad"
        })
        self.assertFalse(review_form.is_valid())
        self.assertIn("rating", review_form.errors.keys())
        self.assertEqual(
            review_form.errors["rating"][0],
            "This field is required."
        )

    def test_review_form_rating_must_be_more_than__or_equal_1(self):
        """
        Asserts the review form is invalid with a rating value <1.
        Asserts the error raised as a result of the incorrect value stems
        from the "rating" key.
        Asserts the error raises matches the expected error.
        """
        review_form = ReviewForm({
            "book": self.book,
            "title": "Test Title",
            "rating": 0,
            "comment": "Not bad"
        })
        self.assertFalse(review_form.is_valid())
        self.assertIn("rating", review_form.errors.keys())
        self.assertEqual(
            review_form.errors["rating"][0],
            "Ensure this value is greater than or equal to 1."
        )

    def test_review_form_rating_must_be_less_than_or_equal_10(self):
        """
        Asserts the review form is invalid with a rating value >10.
        Asserts the error raised as a result of the incorrect value stems
        from the "rating" key.
        Asserts the error raises matches the expected error.
        """
        review_form = ReviewForm({
            "book": self.book,
            "title": "Test Title",
            "rating": 13,
            "comment": "Not bad"
        })
        self.assertFalse(review_form.is_valid())
        self.assertIn("rating", review_form.errors.keys())
        self.assertEqual(
            review_form.errors["rating"][0],
            "Ensure this value is less than or equal to 10."
        )

    def test_review_form_comment_is_required(self):
        """
        Asserts the review form is invalid with an empty comment value.
        Asserts the error raised as a result of the incorrect value stems
        from the "comment" key.
        Asserts the error raises matches the expected error.
        """
        review_form = ReviewForm({
            "book": self.book,
            "title": "Test Title",
            "rating": 8,
            "comment": ""
        })
        self.assertFalse(review_form.is_valid())
        self.assertIn("comment", review_form.errors.keys())
        self.assertEqual(
            review_form.errors["comment"][0],
            "This field is required."
        )

    def test_review_form_is_valid(self):
        """
        Asserts a review form instance that is full and
        correctly filled out is valid.
        """
        review_form = ReviewForm({
            "book": self.book,
            "title": "",
            "rating": 4,
            "comment": "Not bad"
        })
        self.assertFalse(review_form.is_valid())
