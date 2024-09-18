from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify

from .models import Author, Genre, Book
from reader.models import UserProfile


class TestLibraryViews(TestCase):
    """
    A class for testing all views associated with the Library app.Testing scope
    includes testing correct redirection, status codes and template usage.

    Methods:
    def setUp():
        REGISTRATION:
            Simulates user registration to allow for users to create an
            author profile to allow for the creation of a book.

        USER & AUTHOR PROFILES:
            A user profile is created automatically following successful
            registration and retrieved. This profile is associated with
            an author profile.

        GENRE + BOOK:
            A test genre is created and assigned to the test book instance.
            This instance is used in the testing of URLs in POST requests.

        Saves the relevant models to the test sqlite3 database.
        Retrieves the relevant URLs and assigns them to variables for testing.


    def test_library_q_get_request_is_successful():
        Retrieves the library URL with a request for a specific keyword
        to be included in the book title (via search bar) and asserts
        the view renders successfully.
        Asserts the template used matches the expected template defined in
        views.py.


    def test_library_author_get_request_is_successful():
        Retrieves the library URL with a request for a specific author
        (via filters) and asserts the view renders successfully.
        Asserts the view status code is 200.
        Asserts the template used matches the expected template defined in
        views.py.


    def test_library_genre_get_request_is_successful():
        Retrieves the library URL with a request for a specific genre
        (via filters) and asserts the view renders successfully.
        Asserts the view status code is 200.
        Asserts the template used matches the expected template defined in
        views.py.


    def test_book_detail_get_request_is_successful():
        Retrieves the book detail URL with a book slug argument and asserts
        the view renders successfully.
        Asserts the view status code is 200.
        Asserts the template used matches the expected template defined in
        views.py.
    """

    def setUp(self):
        """
        REGISTRATION:
            Simulates user registration to allow for users to create an
            author profile to allow for the creation of a book.

        USER & AUTHOR PROFILES:
            A user profile is created automatically following successful
            registration and retrieved. This profile is associated with
            an author profile.

        GENRE + BOOK:
            A test genre is created and assigned to the test book instance.
            This instance is used in the testing of URLs in POST requests.

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

        self.library_url = reverse("library")
        self.book_detail_url = reverse(
            "book-summary", args=[self.book.slug]
        )

    def test_library_q_get_request_is_successful(self):
        """
        Retrieves the library URL with a request for a specific keyword
        to be included in the book title (via search bar) and asserts
        the view renders successfully.
        Asserts the template used matches the expected template defined in
        views.py.
        """
        res = self.client.get(self.library_url, {"q": "the"})
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "library/library.html")

    def test_library_author_get_request_is_successful(self):
        """
        Retrieves the library URL with a request for a specific author
        (via filters) and asserts the view renders successfully.
        Asserts the view status code is 200.
        Asserts the template used matches the expected template defined in
        views.py.
        """
        res = self.client.get(self.library_url, {"author": "dick"})
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "library/library.html")

    def test_library_genre_get_request_is_successful(self):
        """
        Retrieves the library URL with a request for a specific genre
        (via filters) and asserts the view renders successfully.
        Asserts the view status code is 200.
        Asserts the template used matches the expected template defined in
        views.py.
        """
        res = self.client.get(self.library_url, {"genre": "adventure"})
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "library/library.html")

    def test_book_detail_get_request_is_successful(self):
        """
        Retrieves the book detail URL with a book slug argument and asserts
        the view renders successfully.
        Asserts the view status code is 200.
        Asserts the template used matches the expected template defined in
        views.py.
        """
        res = self.client.get(self.book_detail_url, args=[self.book.slug])
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "library/book_detail.html")
