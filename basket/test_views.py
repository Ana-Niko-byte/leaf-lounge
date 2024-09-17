from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify

from library.models import Author, Genre, Book
from reader.models import UserProfile


class TestBasketViews(TestCase):
    """
    A class to test views associated with the Basket app. Testing scope
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


    def test_basket_get_request_is_retrieved():
        Retrieves the basket URL and asserts the view renders successfully.
        Asserts the view status code is 200.
        Asserts the template used matches the expected template defined in
        views.py.


    def test_add_to_basket_post_request_is_retrieved():
        Retrieves the add_to_basket URL and asserts the view handles post data.
        Asserts the view redirects after data handling.
        Asserts the client is redirected to the correct URL, correctly
        redirects and has a status code of 302 indicating redirection, a
        target status of 200 meaning the view is rendered correctly.


    def test_update_basket_post_request_is_resolved():
        Retrieves the update_basket URL and asserts the view handles post data.
        Asserts the view redirects after data handling.
        Asserts the client is redirected to the correct URL, correctly
        redirects and has a status code of 302 indicating redirection, a target
        status of 200 meaning the view is rendered correctly.


    def test_delete_from_basket_post_request_is_resolved():
        Retrieves the delete_from_basket URL and asserts the view handles
        post data.
        Asserts the view status code is 200.
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

        self.basket_url = reverse("basket")
        self.add_to_basket_url = reverse("add_to_basket", args=[self.book.id])
        self.update_basket_url = reverse("update_basket", args=[self.book.id])
        self.delete_from_basket_url = reverse(
            "delete_basket", args=[self.book.id]
        )

    def test_basket_get_request_is_retrieved(self):
        """
        Retrieves the basket URL and asserts the view renders successfully.
        Asserts the view status code is 200.
        Asserts the template used matches the expected template defined in
        views.py.
        """
        res = self.client.post(self.basket_url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "basket/basket.html")

    def test_add_to_basket_post_request_is_retrieved(self):
        """
        Retrieves the add_to_basket URL and asserts the view handles post data.
        Asserts the view redirects after data handling.
        Asserts the client is redirected to the correct URL, the view correctly
        redirects and has a status code of 302 indicating redirection, and a
        target status of 200 meaning the view is rendered correctly.
        """
        res = self.client.post(self.add_to_basket_url, {"quantity": 5})
        self.assertRedirects(
            res, f'/library/book/{self.book.slug}/', status_code=302,
            target_status_code=200, fetch_redirect_response=True
        )

    def test_update_basket_post_request_is_resolved(self):
        """
        Retrieves the update_basket URL and asserts the view handles post data.
        Asserts the view redirects after data handling.
        Asserts the client is redirected to the correct URL, the view correctly
        redirects and has a status code of 302 indicating redirection, and a
        target status of 200 meaning the view is rendered correctly.
        """
        res = self.client.post(self.update_basket_url, {"quantity": 2})
        self.assertRedirects(
            res, f'/basket/', status_code=302, target_status_code=200,
            fetch_redirect_response=True
        )

    def test_delete_from_basket_post_request_is_resolved(self):
        """
        Retrieves the delete_from_basket URL and asserts the view handles
        post data.
        Asserts the view status code is 200.
        """
        res = self.client.post(self.delete_from_basket_url, {"quantity": 2})
        self.assertEqual(res.status_code, 200)
