from django.test import TestCase, Client
from django.urls import reverse


class TestMarketingViews(TestCase):
    """
    A class to test views associated with the Marketing app. Testing scope
    includes testing correct redirection and redirection status codes.

    Methods:
    def setUp():
        Retrieves the relevant URLs and assigns them to variables for testing.


    def test_subscribe_post_request_is_successful():
        Simulates form data passed to the subscribe form for testing a POST
        request.
        Asserts the client is redirected to the correct URL if the view
        receives correct form data, the view correctly redirects and has a
        status code of 302 indicating redirection, and a target status of 200
        meaning the view is rendered correctly.


    def test_unsubscribe_post_request_is_successful():
        Simulates form data passed to the unsubscribe form for testing a POST
        request.
        Asserts the client is redirected to the correct URL if the view
        receives correct form data, the view correctly redirects and has a
        status code of 302 indicating redirection, and a target status of 200
        meaning the view is rendered correctly.
    """

    def setUp(self):
        """
        Retrieves the relevant URLs and assigns them to variables for testing.
        """
        self.subscribe_url = reverse("subscribe")
        self.unsubscribe_url = reverse("unsubscribe")

    def test_subscribe_post_request_is_successful(self):
        """
        Simulates form data passed to the subscribe form for testing a POST
        request.
        Asserts the client is redirected to the correct URL if the view
        receives correct form data, the view correctly redirects and has a
        status code of 302 indicating redirection, and a target status of 200
        meaning the view is rendered correctly.
        """
        mock_form = {
            "email": "tester@email.com"
        }
        res = self.client.post(self.subscribe_url, data=mock_form)
        self.assertRedirects(
            res, "/", status_code=302, target_status_code=200,
            fetch_redirect_response=True
        )

    def test_unsubscribe_post_request_is_successful(self):
        """
        Simulates form data passed to the unsubscribe form for testing a POST
        request.
        Asserts the client is redirected to the correct URL if the view
        receives correct form data, the view correctly redirects and has a
        status code of 302 indicating redirection, and a target status of 200
        meaning the view is rendered correctly.
        """
        mock_form = {
            "email": "tester@email.com"
        }
        res = self.client.post(self.unsubscribe_url, data=mock_form)
        self.assertRedirects(
            res, "/", status_code=302, target_status_code=200,
            fetch_redirect_response=True
        )
