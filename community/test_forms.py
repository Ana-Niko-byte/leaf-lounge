from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client

from .forms import *


class TestAuthorForm(TestCase):
    """
    A class for testing the Author Form associated with the community app.
    This form allows registered users to create an Author Profile account
    so that they can register and upload books onto the Leaf Lounge website.

    Methods:
    def setUp(self):
        REGISTRATION:
            Simulates user registration to allow for the creation of a user
            profile.

        USER PROFILE & AUTHOR PROFILE:
            Retrieves the user profile automatically created following
            successful user registration. This is handled via
            reader.signals.create_or_save_profile.
            Simulates the creation of an author profile and assigns the
            relevant user profile to the author.user_profile field.

        Saves the relevant models to the test sqlite3 database.


    def test_user_profile_is_not_required():
        Asserts an Author profile can be created without an associated
        user profile - this is specifically for authors uploaded via the
        admin panel. This is not representative of authors created by Leaf
        Lounge users.


    def test_first_name_is_required():
        Asserts the author form is invalid with an empty first_name value.
        Asserts the error raised as a result of the incorrect value stems
        from the "first_name" key.
        Asserts the error raises matches the expected error.


    def test_last_name_is_required():
        Asserts the author form is invalid with an empty last_name value.
        Asserts the error raised as a result of the incorrect value stems
        from the "last_name" key.
        Asserts the error raises matches the expected error.


    def test_d_o_b_is_required():
        Asserts the author form is invalid with an empty d_o_b value.
        Asserts the error raised as a result of the incorrect value stems
        from the "d_o_b" key.
        Asserts the error raises matches the expected error.


    def test_d_o_b_must_be_correct_format():
        Asserts the author form is invalid with an incorrectly formatted d_o_b
        value, which should follow YYYY-MM-DD.
        Asserts the error raised as a result of the incorrect value stems
        from the "d_o_b" key.
        Asserts the error raises matches the expected error. The formatting of
        this is handled automatically via the form. This test checks bad user
        injection.


    def test_nationality_is_not_required():
        Asserts the author form is valid even if no value for the
        Nationality was provided.


    def test_bio_is_required():
        Asserts the author form is invalid with an empty bio value.
        Asserts the error raised as a result of the incorrect value stems
        from the "bio" key.
        Asserts the error raises matches the expected error.


    def test_fully_and_correctly_filled_form_is_valid():
        Asserts the author form is valid when all information is provided.
    """

    def setUp(self):
        """
        REGISTRATION:
            Simulates user registration to allow for the creation of a user
            profile.

        USER PROFILE & AUTHOR PROFILE:
            Retrieves the user profile automatically created following
            successful user registration. This is handled via
            reader.signals.create_or_save_profile.
            Simulates the creation of an author profile and assigns the
            relevant user profile to the author.user_profile field.

        Saves the relevant models to the test sqlite3 database.
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

    def test_user_profile_is_not_required(self):
        """
        Asserts an Author profile can be created without an associated
        user profile - this is specifically for authors uploaded via the
        admin panel. This is not representative of authors created by Leaf
        Lounge users.
        """
        author_form = AuthorForm({
            "user_profile": "",
            "first_name": "Tester",
            "last_name": "Tester",
            "d_o_b": "2002-04-28",
            "nationality": "IE",
            "bio": "Test",
        })
        self.assertTrue(author_form.is_valid())

    def test_first_name_is_required(self):
        """
        Asserts the author form is invalid with an empty first_name value.
        Asserts the error raised as a result of the incorrect value stems
        from the "first_name" key.
        Asserts the error raises matches the expected error.
        """
        author_form = AuthorForm({
            "user_profile": self.user_profile,
            "first_name": "",
            "last_name": "Tester",
            "d_o_b": "2002-04-28",
            "nationality": "IE",
            "bio": "Test",
        })
        self.assertFalse(author_form.is_valid())
        self.assertIn("first_name", author_form.errors.keys())
        self.assertEqual(
            author_form.errors["first_name"][0],
            "This field is required."
        )

    def test_last_name_is_required(self):
        """
        Asserts the author form is invalid with an empty last_name value.
        Asserts the error raised as a result of the incorrect value stems
        from the "last_name" key.
        Asserts the error raises matches the expected error.
        """
        author_form = AuthorForm({
            "user_profile": self.user_profile,
            "first_name": "Tester",
            "last_name": "",
            "d_o_b": "2002-04-28",
            "nationality": "IE",
            "bio": "Test",
        })
        self.assertFalse(author_form.is_valid())
        self.assertIn("last_name", author_form.errors.keys())
        self.assertEqual(
            author_form.errors["last_name"][0],
            "This field is required."
        )

    def test_d_o_b_is_required(self):
        """
        Asserts the author form is invalid with an empty d_o_b value.
        Asserts the error raised as a result of the incorrect value stems
        from the "d_o_b" key.
        Asserts the error raises matches the expected error.
        """
        author_form = AuthorForm({
            "user_profile": self.user_profile,
            "first_name": "Tester",
            "last_name": "Tester",
            "d_o_b": "",
            "nationality": "IE",
            "bio": "Test",
        })
        self.assertFalse(author_form.is_valid())
        self.assertIn("d_o_b", author_form.errors.keys())
        self.assertEqual(
            author_form.errors["d_o_b"][0],
            "This field is required."
        )

    def test_d_o_b_must_be_correct_format(self):
        """
        Asserts the author form is invalid with an incorrectly formatted d_o_b
        value, which should follow YYYY-MM-DD.
        Asserts the error raised as a result of the incorrect value stems
        from the "d_o_b" key.
        Asserts the error raises matches the expected error. The formatting of
        this is handled automatically via the form. This test checks bad user
        injection.
        """
        author_form = AuthorForm({
            "user_profile": self.user_profile,
            "first_name": "Tester",
            "last_name": "Tester",
            "d_o_b": "2002/04/28",
            "nationality": "IE",
            "bio": "Test",
        })
        self.assertFalse(author_form.is_valid())
        self.assertIn("d_o_b", author_form.errors.keys())
        self.assertEqual(
            author_form.errors["d_o_b"][0],
            "Enter a valid date."
        )

    def test_nationality_is_not_required(self):
        """
        Asserts the author form is valid even if no value for the
        Nationality was provided.
        """
        author_form = AuthorForm({
            "user_profile": self.user_profile,
            "first_name": "Tester",
            "last_name": "Tester",
            "d_o_b": "2002-04-28",
            "nationality": "",
            "bio": "Test",
        })
        self.assertTrue(author_form.is_valid())

    def test_bio_is_required(self):
        """
        Asserts the author form is invalid with an empty bio value.
        Asserts the error raised as a result of the incorrect value stems
        from the "bio" key.
        Asserts the error raises matches the expected error.
        """
        author_form = AuthorForm({
            "user_profile": self.user_profile,
            "first_name": "Tester",
            "last_name": "Tester",
            "d_o_b": "2002-04-28",
            "nationality": "IE",
            "bio": "",
        })
        self.assertFalse(author_form.is_valid())
        self.assertIn("bio", author_form.errors.keys())
        self.assertEqual(
            author_form.errors["bio"][0],
            "This field is required."
        )

    def test_fully_and_correctly_filled_form_is_valid(self):
        """
        Asserts the author form is valid when all information is provided.
        """
        author_form = AuthorForm({
            "user_profile": self.user_profile,
            "first_name": "Tester",
            "last_name": "Tester",
            "d_o_b": "2002-04-28",
            "nationality": "IE",
            "bio": "Test",
        })
        self.assertTrue(author_form.is_valid())


class TestBookForm(TestCase):
    """
    A class for testing the Book Registration Form associated with the
    community app.
    This form allows registered users with associated profile accounts to
    register their books. These books can be viewed under "My Books" in the
    secondary navigation bar.

    Methods:
        def setUp():
        REGISTRATION:
            Simulates user registration to allow for the creation of a user
            profile.

        USER PROFILE & AUTHOR PROFILE:
            Retrieves the user profile automatically created following
            successful user registration. This is handled via
            reader.signals.create_or_save_profile.
            Simulates the creation of an author profile and assigns the
            relevant user profile to the author.user_profile field.

        GENRE & COMMUNITY:
            Simulates the creation of a genre.

        Saves the relevant models to the test sqlite3 database.

    def missing_field_assertion():
        A helper function used for running assertion tests for missing
        values in form fields.

        Arguments:
        value: str - the form field being tested.
        form: obj - the form being tested.


    def test_book_form_title_is_required():
        Asserts the book form is invalid with an empty title value.
        Asserts the error raised as a result of the incorrect value stems
        from the "title" key.
        Asserts the error raises matches the expected error.


    def test_book_form_isbn_is_required():
        Asserts the book form is invalid with an empty isbn value.
        Asserts the error raised as a result of the incorrect value stems
        from the "isbn" key.
        Asserts the error raises matches the expected error.


    def test_book_form_blurb_is_required():
        Asserts the book form is invalid with an empty blurb value.
        Asserts the error raised as a result of the incorrect value stems
        from the "blurb" key.
        Asserts the error raises matches the expected error.


    def test_book_form_genre_is_required():
        Asserts the book form is invalid with an empty genre value.
        Asserts the error raised as a result of the incorrect value stems
        from the "genre" key.
        Asserts the error raises matches the expected error.


    def test_book_form_year_published_is_not_required():
        Asserts the book form is valid without a year_published value.


    def test_book_form_publisher_is_not_required():
        Asserts the book form is valid without a publisher value.


    def test_book_form_type_is_required():
        Asserts the book form is invalid with an empty type value.
        Asserts the error raised as a result of the incorrect value stems
        from the "type" key.
        Asserts the error raises matches the expected error.


    def test_book_form_type_must_be_one_of_predefined():
        Asserts the book form is invalid with an incorrect type value.
        Asserts the error raised as a result of the incorrect value stems
        from the "type" key.
        Asserts the error raises matches the expected error.


    def test_book_form_price_is_required():
        Asserts the book form is invalid with an empty price value.
        Asserts the error raised as a result of the incorrect value stems
        from the "price" key.
        Asserts the error raises matches the expected error.


    def test_book_form_price_must_be_under_5_digits():
        Asserts the book form is invalid if a price value over 5 digits
        is provided for books.
        Asserts the error raised as a result of the incorrect value stems
        from the "price" key.
        Asserts the error raises matches the expected error.


    def test_test_correctly_filled_form_is_valid():
        Asserts a correctly filled form is valid.
    """
    def setUp(self):
        """
        REGISTRATION:
            Simulates user registration to allow for the creation of a user
            profile.

        USER PROFILE & AUTHOR PROFILE:
            Retrieves the user profile automatically created following
            successful user registration. This is handled via
            reader.signals.create_or_save_profile.
            Simulates the creation of an author profile and assigns the
            relevant user profile to the author.user_profile field.

        GENRE & COMMUNITY:
            Simulates the creation of a genre.

        Saves the relevant models to the test sqlite3 database.
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

    def missing_field_assertion(self, value, form):
        """
        A helper function used for running assertion tests for missing
        values in form fields.

        Arguments:
        value: str - the form field being tested.
        form: obj - the form being tested.
        """
        self.assertFalse(form.is_valid())
        self.assertIn(value, form.errors.keys())
        self.assertEqual(
            form.errors[value][0],
            "This field is required."
        )

    def test_book_form_title_is_required(self):
        """
        Asserts the book form is invalid with an empty title value.
        Asserts the error raised as a result of the incorrect value stems
        from the "title" key.
        Asserts the error raises matches the expected error.
        """
        book_form = BookForm({
            "title": "",
            "isbn": "0-061-96436-0",
            "blurb": "Test blurb",
            "genre": self.genre,
            "year_published": "2000",
            "publisher": "Test Publisher",
            "type": "Hardback",
            "price": "14.99"
        })
        self.missing_field_assertion("title", book_form)

    def test_book_form_isbn_is_required(self):
        """
        Asserts the book form is invalid with an empty isbn value.
        Asserts the error raised as a result of the incorrect value stems
        from the "isbn" key.
        Asserts the error raises matches the expected error.
        """
        book_form = BookForm({
            "title": "Test Title",
            "isbn": "",
            "blurb": "Test blurb",
            "genre": self.genre,
            "year_published": "2000",
            "publisher": "Test Publisher",
            "type": "Hardback",
            "price": "14.99"
        })
        self.missing_field_assertion("isbn", book_form)

    def test_book_form_blurb_is_required(self):
        """
        Asserts the book form is invalid with an empty blurb value.
        Asserts the error raised as a result of the incorrect value stems
        from the "blurb" key.
        Asserts the error raises matches the expected error.
        """
        book_form = BookForm({
            "title": "Test Title",
            "isbn": "0-061-96436-0",
            "blurb": "",
            "genre": self.genre,
            "year_published": "2000",
            "publisher": "Test Publisher",
            "type": "Hardback",
            "price": "14.99"
        })
        self.missing_field_assertion("blurb", book_form)

    def test_book_form_genre_is_required(self):
        """
        Asserts the book form is invalid with an empty genre value.
        Asserts the error raised as a result of the incorrect value stems
        from the "genre" key.
        Asserts the error raises matches the expected error.
        """
        book_form = BookForm({
            "title": "Test Title",
            "isbn": "0-061-96436-0",
            "blurb": "Test Blurb",
            "genre": None,
            "year_published": "2000",
            "publisher": "Test Publisher",
            "type": "Hardback",
            "price": "14.99"
        })
        self.missing_field_assertion("genre", book_form)

    def test_book_form_year_published_is_not_required(self):
        """
        Asserts the book form is valid without a year_published value.
        """
        book_form = BookForm({
            "title": "Test Title",
            "isbn": "0-061-96436-0",
            "blurb": "Test Blurb",
            "genre": self.genre,
            "year_published": "",
            "publisher": "Test Publisher",
            "type": "Hardback",
            "price": "14.99"
        })
        self.assertTrue(book_form.is_valid)

    def test_book_form_publisher_is_not_required(self):
        """
        Asserts the book form is valid without a publisher value.
        """
        book_form = BookForm({
            "title": "Test Title",
            "isbn": "0-061-96436-0",
            "blurb": "Test Blurb",
            "genre": self.genre,
            "year_published": "2000",
            "publisher": "",
            "type": "Hardback",
            "price": "14.99"
        })
        self.assertTrue(book_form.is_valid())

    def test_book_form_type_is_required(self):
        """
        Asserts the book form is invalid with an empty type value.
        Asserts the error raised as a result of the incorrect value stems
        from the "type" key.
        Asserts the error raises matches the expected error.
        """
        book_form = BookForm({
            "title": "Test Title",
            "isbn": "0-061-96436-0",
            "blurb": "Test Blurb",
            "genre": self.genre,
            "year_published": "2000",
            "publisher": "Test Publisher",
            "type": "",
            "price": "14.99"
        })
        self.missing_field_assertion("type", book_form)

    def test_book_form_type_must_be_one_of_predefined(self):
        """
        Asserts the book form is invalid with an incorrect type value.
        Asserts the error raised as a result of the incorrect value stems
        from the "type" key.
        Asserts the error raises matches the expected error.
        """
        book_form = BookForm({
            "title": "Test Title",
            "isbn": "0-061-96436-0",
            "blurb": "Test Blurb",
            "genre": self.genre,
            "year_published": "2000",
            "publisher": "Test Publisher",
            "type": "Not",
            "price": "14.99"
        })
        self.assertFalse(book_form.is_valid())
        self.assertIn("type", book_form.errors.keys())
        self.assertEqual(
            book_form.errors["type"][0],
            "Select a valid choice. Not is not one of the available choices."
        )

    def test_book_form_price_is_required(self):
        """
        Asserts the book form is invalid with an empty price value.
        Asserts the error raised as a result of the incorrect value stems
        from the "price" key.
        Asserts the error raises matches the expected error.
        """
        book_form = BookForm({
            "title": "Test Title",
            "isbn": "0-061-96436-0",
            "blurb": "Test Blurb",
            "genre": self.genre,
            "year_published": "2000",
            "publisher": "Test Publisher",
            "type": "Hardback",
            "price": ""
        })
        self.missing_field_assertion("price", book_form)

    def test_book_form_price_must_be_under_5_digits(self):
        """
        Asserts the book form is invalid if a price value over 5 digits
        is provided for books.
        Asserts the error raised as a result of the incorrect value stems
        from the "price" key.
        Asserts the error raises matches the expected error.
        """
        book_form = BookForm({
            "title": "Test Title",
            "isbn": "0-061-96436-0",
            "blurb": "Test Blurb",
            "genre": self.genre,
            "year_published": "2000",
            "publisher": "Test Publisher",
            "type": "Hardback",
            "price": 1200.99
        })
        self.assertFalse(book_form.is_valid())
        self.assertIn("price", book_form.errors.keys())
        self.assertEqual(
            book_form.errors["price"][0],
            "Ensure that there are no more than 5 digits in total."
        )

    def test_test_correctly_filled_form_is_valid(self):
        """
        Asserts a correctly filled form is valid.
        """
        book_form = BookForm({
            "title": "Test Title",
            "isbn": "0-061-96436-0",
            "blurb": "Test blurb",
            "genre": self.genre,
            "year_published": "2000",
            "publisher": "Test Publisher",
            "type": "Hardback",
            "price": "14.99"
        })
        self.assertTrue(book_form.is_valid())


class TestForumForm(TestCase):
    """
    A class for testing the Forum form associated with the community app.
    This form allows users to create chat forums within genre communities.

    Methods:
    def test_forum_form_name_is_required():
        Asserts the forum form is invalid with an empty name value.
        Asserts the error raised as a result of the incorrect value stems
        from the "name" key.
        Asserts the error raises matches the expected error.


    def test_filled_forum_form_is_valid():
        Asserts a correctly filled form is valid.
    """
    def test_forum_form_name_is_required(self):
        """
        Asserts the forum form is invalid with an empty name value.
        Asserts the error raised as a result of the incorrect value stems
        from the "name" key.
        Asserts the error raises matches the expected error.
        """
        forum_form = ForumForm({
            "name": ""
        })
        self.assertFalse(forum_form.is_valid())
        self.assertIn("name", forum_form.errors.keys())
        self.assertEqual(
            forum_form.errors["name"][0],
            "This field is required."
        )

    def test_filled_forum_form_is_valid(self):
        """
        Asserts a correctly filled form is valid.
        """
        forum_form = ForumForm({
            "name": "Test Forum"
        })
        self.assertTrue(forum_form.is_valid())


class TestMessageForm(TestCase):
    """
    A class for testing the Message form associated with the community app.
    This form allows users to send messages within forums.

    Methods:
    def test_forum_form_name_is_required():
        Asserts the message form is invalid with an empty content value.
        Asserts the error raised as a result of the incorrect value stems
        from the "content" key.
        Asserts the error raises matches the expected error.


    def test_filled_message_form_is_valid():
        Asserts a correctly filled form is valid.
    """
    def test_forum_form_name_is_required(self):
        """
        Asserts the message form is invalid with an empty content value.
        Asserts the error raised as a result of the incorrect value stems
        from the "content" key.
        Asserts the error raises matches the expected error.
        """
        message_form = MessageForm({
            "content": ""
        })
        self.assertFalse(message_form.is_valid())
        self.assertIn("content", message_form.errors.keys())
        self.assertEqual(
            message_form.errors["content"][0],
            "This field is required."
        )

    def test_filled_message_form_is_valid(self):
        """
        Asserts a correctly filled form is valid.
        """
        message_form = MessageForm({
            "content": "test message"
        })
        self.assertTrue(message_form.is_valid())
