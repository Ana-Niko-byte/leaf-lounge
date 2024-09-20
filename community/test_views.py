from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone

from library.models import Author, Genre, Book, Review
from .models import *


class TestCommunityViews(TestCase):
    """
    A class for testing all views associated with the Community app. Testing
    scope includes testing correct redirection, status codes and template
    usage.

    Methods:
    def setUp():
        REGISTRATION:
            Simulates user registration to allow for users to create an
            author profile to allow for the creation of a book.

        USER & AUTHOR PROFILES:
            A user profile is created automatically following successful
            registration and retrieved. This profile is associated with
            an author profile.

        GENRE & COMMUNITY & FORUM:
            Simulates the creation of a genre. After the mock genre
            is saved, a community is automatically created. After
            the community is saved, forums can be created inside the
            community.
            Simulates the creation of a forum and saves it.

        MESSAGE:
            Simulates the creation of a message and saves it.

        Saves the relevant models to the test sqlite3 database.
        Retrieves the relevant URLs and assigns them to variables for testing.


    def test_communities_get_request_is_successful():
        Retrieves the communities URL and asserts the view renders
        successfully.
        Asserts the status code is 200.
        Asserts the template used matches the expected template defined in
        views.py.


    def test_specific_community_get_request_is_successful():
        Retrieves a specific community URL and asserts the view renders
        successfully.
        Asserts the status code is 200.
        Asserts the template used matches the expected template defined in
        views.py.


    def test_forum_get_request_is_successful():
        Retrieves a specific forum URL and asserts the view renders
        successfully.
        Asserts the status code is 200.
        Asserts the template used matches the expected template defined in
        views.py.


    def test_forum_post_request_is_successful():
        Retrieves the forum URL and asserts the view handles POST
        requests.
        Asserts the view redirects to the correct URL after a message is
        created, the status code is 302 signifying redirection, the status of
        the view being redirected to is 200, and that the redirection was
        performed correctly.


    def test_forum_message_deletion():
        Retrieves the message_delete URL and asserts the view handles DELETE
        requests.
        Asserts the view redirects to the correct URL following deletion, the
        status code is 302 signifying redirection, the status of the view being
        redirected to is 200, and that the redirection was performed correctly.


    def test_create_author_get_request_is_successful():
        Retrieves the create_author URL and asserts the view renders
        successfully.
        Asserts the status code is 200.
        Asserts the template used matches the expected template defined in
        views.py.


    def test_create_author_post_request_is_successful():
        Retrieves the create_author URL and asserts the view handles POST
        requests.
        Asserts the view redirects to the correct URL - the
        upload_book URL through which new book instances are created, the
        status code is 302 signifying redirection, the status of the view being
        redirected to is 200, and that the redirection was performed correctly.
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

        GENRE & COMMUNITY & FORUM:
            Simulates the creation of a genre. After the mock genre
            is saved, a community is automatically created. After
            the community is saved, forums can be created inside the
            community.
            Simulates the creation of a forum and saves it.

        MESSAGE:
            Simulates the creation of a message and saves it.

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

        self.communities_url = reverse("communities")
        self.community_url = reverse(
            "community", args=[self.genre.community.slug]
        )
        self.forum_url = reverse("forum_detail", args=[self.forum.slug])
        self.become_author_url = reverse("create_author")
        self.upload_book_url = reverse("upload_book")
        self.delete_message_url = reverse(
            "delete_message", args=[self.forum.slug, self.message.id]
        )

    def test_communities_get_request_is_successful(self):
        """
        Retrieves the communities URL and asserts the view renders
        successfully.
        Asserts the status code is 200.
        Asserts the template used matches the expected template defined in
        views.py.
        """
        res = self.client.get(self.communities_url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "community/community.html")

    def test_specific_community_get_request_is_successful(self):
        """
        Retrieves a specific community URL and asserts the view renders
        successfully.
        Asserts the status code is 200.
        Asserts the template used matches the expected template defined in
        views.py.
        """
        res = self.client.get(self.community_url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "community/community_detail.html")

    def test_forum_get_request_is_successful(self):
        """
        Retrieves a specific forum URL and asserts the view renders
        successfully.
        Asserts the status code is 200.
        Asserts the template used matches the expected template defined in
        views.py.
        """
        res = self.client.get(self.forum_url, args=[self.forum.slug])
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "community/forum_detail.html")

    def test_forum_post_request_is_successful(self):
        """
        Retrieves the forum URL and asserts the view handles POST
        requests.
        Asserts the view redirects to the correct URL after a message is
        created, the status code is 302 signifying redirection, the status of
        the view being redirected to is 200, and that the redirection was
        performed correctly.
        """
        message_data = {
            "content": "Test Message"
        }
        res = self.client.post(self.forum_url, args=[self.forum.slug])
        self.assertRedirects(
            res, f"/community/forum/{self.forum.slug}", status_code=302,
            target_status_code=200, fetch_redirect_response=True
        )

    def test_forum_message_deletion(self):
        """
        Retrieves the message_delete URL and asserts the view handles DELETE
        requests.
        Asserts the view redirects to the correct URL following deletion, the
        status code is 302 signifying redirection, the status of the view being
        redirected to is 200, and that the redirection was performed correctly.
        """
        res = self.client.delete(
            self.delete_message_url, args=[self.forum.slug, self.message.id]
        )
        self.assertRedirects(
            res, f"/community/forum/{self.forum.slug}", status_code=302,
            target_status_code=200, fetch_redirect_response=True
        )

    def test_create_author_get_request_is_successful(self):
        """
        Retrieves the create_author URL and asserts the view renders
        successfully.
        Asserts the status code is 200.
        Asserts the template used matches the expected template defined in
        views.py.
        """
        res = self.client.get(self.become_author_url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "community/create_author.html")

    def test_create_author_post_request_is_successful(self):
        """
        Retrieves the create_author URL and asserts the view handles POST
        requests.
        Asserts the view redirects to the correct URL - the
        upload_book URL through which new book instances are created, the
        status code is 302 signifying redirection, the status of the view being
        redirected to is 200, and that the redirection was performed correctly.
        """
        author_data = {
            "user_profile": self.user_profile,
            "first_name": "Tester",
            "last_name": "Tester",
            "d_o_b": "2002-04-28",
            "nationality": "IE",
            "bio": "Test"
        }
        res = self.client.post(self.become_author_url, data=author_data)
        self.assertRedirects(
            res, self.upload_book_url, status_code=302,
            target_status_code=200, fetch_redirect_response=True
        )
