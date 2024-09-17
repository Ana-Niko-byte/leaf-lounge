from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings


class TestBlurbViews(TestCase):
    """
    A class to test views associated with the Blurb app. Testing scope
    includes testing correct redirection, status codes and template usage.

    Methods:
    def setUp():
        Retrieves the relevant URLs and assigns them to variables for testing.


    def test_home_page_is_retrieved():
        Retrieves the home page URL and asserts the view renders successfully.
        Asserts the view status code is 200.
        Asserts the template used matches the expected template defined in
        views.py.


    def test_contact_page_get_request_is_retrieved():
        Retrieves the contact page URL and asserts the view renders correctly.
        Asserts the view status code is 200.
        Asserts the template used matches the expected template defines in
        views.py


    def test_contact_page_post_request_is_successful():
        Simulates form data passed to the contact view for testing a POST
        request.
        Asserts the client is redirected to the correct URL if the view receives
        correct contact form data, the view correctly redirects and has a status
        code of 302 indicating redirection, and a target status of 200 meaning
        the view is rendered correctly.
    """

    def setUp(self):
        """
        Retrieves the relevant URLs and assigns them to variables for testing.
        """
        self.home_url = reverse("home")
        self.contact_url = reverse("contact")

    def test_home_page_is_retrieved(self):
        """
        Retrieves the home page URL and asserts the view renders successfully.
        Asserts the view status code is 200.
        Asserts the template used matches the expected template defined in
        views.py.
        """
        res = self.client.get(self.home_url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "blurb/index.html")

    def test_contact_page_get_request_is_retrieved(self):
        """
        Retrieves the contact page URL and asserts the view renders correctly.
        Asserts the view status code is 200.
        Asserts the template used matches the expected template defines in
        views.py
        """
        res = self.client.get(self.contact_url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "blurb/contact.html")

    def test_contact_page_post_request_is_successful(self):
        """
        Simulates form data passed to the contact view for testing a POST
        request.
        Asserts the client is redirected to the correct URL if the view receives
        correct contact form data, the view correctly redirects and has a status
        code of 302 indicating redirection, and a target status of 200 meaning
        the view is rendered correctly.
        """
        test_data = {
            'name': 'Tester',
            'email': 'tester@email.com',
            'subject': 'Career Opportunities',
            'message': 'Hey! Just testing your view.',
            'recipient_list': [settings.EMAIL_HOST_USER, 'tester@email.com']
        }

        res = self.client.post(self.contact_url, data=test_data)
        self.assertRedirects(
            res, "/", status_code=302, target_status_code=200,
            fetch_redirect_response=True
        )
