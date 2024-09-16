from django.test import TestCase
from django.urls import reverse, resolve
from .views import *


class TestLibraryURLs(TestCase):
    """
    A class for testing URLs associated with the library app.
    This class tests urls resolve from their FBVs.

    Methods:
    def test_library_resolves():
        Reverses the URL name and checks if it returns the correct FBV of
        library.

        Asserts the library view (library) is resolved from 'library'.


    def test_book_detail_resolves():
        Reverses the URL name with arguments [slug:slug] and checks if it
        returns the correct FBV of book_detail.

        Asserts book detail views (book_detail) resolve
        from 'book-summary' with slug arguments generated from the book title
        and author last name.
    """

    def test_library_resolves(self):
        """
        Asserts the library view (library) is resolved from 'library'.
        """
        path = reverse('library')
        self.assertEqual(resolve(path).func, library)

    def test_book_detail_resolves(self):
        """
        Asserts book detail views (book_detail) resolve from 'book-summary'
        with slug arguments generated from the book title and author last name.
        """
        path = reverse('book-summary', args=['wuthering-heights-bronte'])
        self.assertEqual(resolve(path).func, book_detail)
