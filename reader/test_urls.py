from django.test import TestCase
from django.urls import reverse, resolve
from .views import *


class TestUserProfileAssociatedURLs(TestCase):
    """
    A class for testing URLs associated with the reader app.
    This class tests urls resolve from their FBVs.

    Methods:
        Reverses the URL name and checks if it returns the correct FBV of
        subscribe.
    """

    def test_user_profile_resolves(self):
        """
        Asserts the user profile view (my_profile) resolves
        from 'user_profile'.
        """
        path = reverse('user_profile')
        self.assertEqual(resolve(path).func, my_profile)

    def test_user_books_resolves(self):
        """
        Asserts the user book storage view (my_books) resolves
        from 'user_books'.
        """
        path = reverse('user_books')
        self.assertEqual(resolve(path).func, my_books)

    def test_review_resolves(self):
        """
        Asserts the view for leaving book reviews (leave_review) resolves
        from 'leave_review' with an int book id argument.
        """
        path = reverse('leave_review', args=[5])
        self.assertEqual(resolve(path).func, leave_review)

    def test_update_review_resolves(self):
        """
        Asserts the view for updating book reviews (update_review) resolves
        from 'update_review' with an int book id argument.
        """
        path = reverse('update_review', args=[5])
        self.assertEqual(resolve(path).func, update_review)

    def test_delete_review_resolves(self):
        """
        Asserts the view for deleting book reviews (delete_review) resolves
        from 'delete_review' with an int book id argument.
        """
        path = reverse('delete_review', args=[5])
        self.assertEqual(resolve(path).func, delete_review)

    def test_admin_approve_review_resolves(self):
        """
        Asserts the view for admins to approve book reviews (approve_review) resolves
        from 'approve_review' with an int book id argument.
        """
        path = reverse('approve_review', args=[5])
        self.assertEqual(resolve(path).func, approve_review)
