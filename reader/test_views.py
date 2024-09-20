from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify

from library.models import Author, Genre, Book, Review
from .models import UserProfile
from .forms import ReviewForm


class TestReaderViews(TestCase):
    """
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

        self.review = Review(
            reviewer=self.user_profile,
            book=self.book,
            title="Test Review Title",
            rating=8,
            comment="Test review content body",
        )
        self.review.save()

        self.profile_url = reverse("user_profile")
        self.user_books_url = reverse("user_books")
        self.leave_review_url = reverse(
            "leave_review", args=[self.book.id]
        )
        self.delete_review_url = reverse(
            "delete_review", args=[self.book.id]
        )
        self.update_review_url = reverse(
            "update_review", args=[self.book.id]
        )
        self.approve_review_url = reverse(
            "approve_review", args=[self.book.id]
        )

    def test_my_profile_get_request_is_successful(self):
        """
        Retrieves the profile URL and asserts the view renders successfully.
        Asserts the status code is 200.
        Asserts the template used matches the expected template defined in
        views.py.
        """
        res = self.client.get(self.profile_url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "reader/profile.html")

    def test_my_profile_post_request_is_successful(self):
        """
        Retrieves the profile URL and posts user address data to it.
        Asserts the view accepts POST data, redirects to the correct URL, the
        status code is 302 signifying redirection, the status of the view being
        redirected to is 200, the correct message comes up, and that the
        redirection was performed correctly.
        """
        user_data = {
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
        res = self.client.post(self.profile_url, data=user_data)
        self.assertRedirects(
            res, "/profile/me/", status_code=302,
            target_status_code=200,
            msg_prefix="Your information has been saved!",
            fetch_redirect_response=True
        )

    def test_user_books_get_request_is_successful(self):
        """
        Retrieves the user_books URL and asserts the view renders successfully.
        Asserts the status code is 200.
        Asserts the template used matches the expected template defined in
        views.py.
        """
        res = self.client.get(self.user_books_url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "reader/profile_books.html")

    def test_user_books_get_specific_genre_request_is_successful(self):
        """
        Retrieves the user_books URL and asserts the view renders successfully.
        Asserts the status code is 200.
        Asserts the template used matches the expected template defined in
        views.py.
        """
        res = self.client.get(self.user_books_url, {"genre": "Adventure"})
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "reader/profile_books.html")

    def test_review_page_get_request_is_successful(self):
        """
        Retrieves the leave_review URL with an argument of a book id, and
        asserts the view renders successfully.
        Asserts the status code is 200.
        Asserts the template used matches the expected template defined in
        views.py.
        """
        res = self.client.get(self.leave_review_url, args=[self.book.id])
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "reader/review.html")

    def test_user_can_leave_a_review(self):
        """
        Retrieves the leave_review URL.
        Asserts the view accepts POST data, redirects to the correct URL, the
        status code is 302 signifying redirection, the status of the view being
        redirected to is 200, and that the redirection was performed correctly.
        """
        review_data = {
            "reviewer": self.user_profile,
            "book": self.book.id,
            "title": "Test Title",
            "rating": 4,
            "comment": "Not bad"
        }
        res = self.client.post(self.leave_review_url, data=review_data)
        self.assertRedirects(
            res, "/profile/my_books/", status_code=302,
            target_status_code=200, fetch_redirect_response=True
        )

    def test_delete_review(self):
        """
        Retrieves the delete_review URL and provides the review id for the
        review to be deleted.
        Asserts the view accepts DELETE data, redirects to the correct URL,
        the status code is 302 signifying redirection, the status of the view
        being redirected to is 200, the correct message comes up, and that the
        redirection was performed correctly.
        """
        res = self.client.delete(self.delete_review_url, args=[self.review.id])
        self.assertRedirects(
            res, "/profile/me/", status_code=302,
            target_status_code=200,
            msg_prefix="Your review was successfully deleted!",
            fetch_redirect_response=True
        )

    def test_update_review_get_request_is_successful(self):
        """
        Retrieves the update_review URL and provides the id of the review for
        updating.
        Asserts the view redirects to the user profile page if a GET request
        is made. This view only handles POST requests.
        """
        res = self.client.get(self.update_review_url, args=[self.book.id])
        self.assertRedirects(
            res, "/profile/me/", status_code=302,
            target_status_code=200, fetch_redirect_response=True
        )

    def test_update_review_post_request_is_successful(self):
        """
        Retrieves the update_review URL and provides the id of the review for
        updating.
        Asserts the view accepts POST data, redirects to the correct URL,
        the status code is 302 signifying redirection, the status of the view
        being redirected to is 200, and that the redirection was performed
        correctly.
        """
        updated_data = {
            "reviewer": self.user_profile,
            "book": self.book.id,
            "title": "Test Title",
            "rating": 8,
            "comment": "Not bad"
        }
        res = self.client.post(self.update_review_url, data=updated_data)
        self.assertRedirects(
            res, "/profile/me/", status_code=302,
            target_status_code=200, fetch_redirect_response=True
        )

    def test_approve_review_is_successful(self):
        """
        Retrieves the approve_review URL and provides the id of the review for
        updating.
        The permissions for this review (admin access only) are handled by
        views.py
        Asserts the view accepts POST data, redirects to the correct URL, the
        status code is 302 signifying redirection, the status of the view being
        redirected to is 200, and that the redirection was performed correctly.
        """
        approve_data = {
            "approved": True
        }
        res = self.client.post(self.update_review_url, data=approve_data)
        self.assertRedirects(
            res, "/profile/me/", status_code=302,
            target_status_code=200, fetch_redirect_response=True
        )
