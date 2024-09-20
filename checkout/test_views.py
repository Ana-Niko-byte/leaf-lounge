from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify

from library.models import Author, Genre, Book
from reader.models import UserProfile
from .models import *


class TestCheckoutViews(TestCase):
    """
    A class to test views associated with the Checkout app. Testing scope
    includes testing correct redirection, status codes and template usage.

    Methods:
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
        Simulates the creation of a genre.

        BOOK:
        Simulates the creation of a book with relevant relationships to the
        author and genre models.

        ORDER & BOOKLINEITEM:
        Simulates the creation of an order with no order number.
        Simulates the creation of a booklineitem, with relevant relationships
        to the order and book models. These models in turn depend on the
        genre, user profile, and author models.

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

        self.order = Order(
            order_number=None,
            user_profile=self.user_profile,
            full_name="Firstname Lastname",
            email="test@gmail.com",
            phone_number="1234567890",
            country="IE",
            postcode="V94 XXXX",
            town_city="Anywhere",
            street_1="Street 1",
            street_2="Street 2",
            county="Anycounty",
            original_basket="test",
            stripe_pid="teststripepid"
        )
        self.order.save()

        self.booklineitem = BookLineItem(
            order=self.order,
            book=self.book,
            type="Softcover",
            quantity=2
        )
        self.booklineitem.save()

        self.checkout_url = reverse("checkout")
        self.checkout_url = reverse("success", args=[self.order.order_number])

    def test_checkout_get_request_is_retrieved(self):
        """
        Retrieves the checkout URL and asserts the view renders successfully.
        Asserts the view status code is 200.
        Asserts the template used matches the expected template defined in
        views.py.
        """
        session = self.client.session
        session["basket"] = {}
        session.save()

        res = self.client.post(self.checkout_url)
        # Not redirecting? - is basket improperly configured?
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse("library"))

    def test_checkout_post_request_is_retrieved(self):
        """
        Retrieves the add_to_basket URL and asserts the view handles post data.
        Asserts the view redirects after data handling.
        Asserts the client is redirected to the correct URL, the view correctly
        redirects and has a status code of 302 indicating redirection, and a
        target status of 200 meaning the view is rendered correctly.
        """
        mock_order = {
            "full_name": "Tester Tester",
            "email": "tester@email.com",
            "phone_number": "123 456 7890",
            "street_1": "Street Address 1",
            "street_2": "Street Address 2",
            "town_city": "Town",
            "postcode": "12345",
            "county": "County",
            "country": "IE"
        }

        res = self.client.post(self.checkout_url, data=mock_order)

        self.assertRedirects(
            res, f'/success/{self.order.order_number}/', status_code=302,
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
