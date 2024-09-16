from django.test import TestCase
from django.urls import reverse, resolve
from .views import *


class TestCommunityURLs(TestCase):
    """
    A class for testing URLs associated with the community app.
    This class tests urls resolve from their FBVs.

    Methods:
    def test_community_general_resolves():
        Reverses the URL name and checks if it returns the correct FBV of
        community_general.

        Asserts the community general view (community) is resolved from
        'communities'.


    def test_community_specific_resolves():
        Reverses the URL name with arguments [slug:slug] and checks if it
        returns the correct FBV of community.

        Asserts specific community views (community) resolve
        from 'community' with slug arguments generated from the
        community name.


    def test_forum_detail_resolves():
        Reverses the URL name with arguments [slug:slug] and checks if it
        returns the correct FBV of forum_detail.

        Asserts the genre-specific forum details (forum_detail) resolve
        from 'forum-detail' with slug arguments generated from the
        forum name.


    def test_author_registration_resolves():
        Reverses the URL name and checks if it returns the correct FBV of
        create_author.

        Asserts the author registration view (create_author) is resolved from
        'create_author'.


    def test_book_registration_resolves():
        Reverses the URL name and checks if it returns the correct FBV of
        upload_book.

        Asserts the book upload/registration view (upload_book) is resolved
        from 'upload_book'.


    def test_delete_message_from_forum_resolves(self):
        Reverses the URL name with arguments [slug:slug] and [int:id] and
        checks if it returns the correct FBV of delete_message.

        Asserts the view for deleting forum messages (delete_message) resolves
        from 'delete_message' with arguments of slug: forum name and
        int: message id.
    """

    def test_community_general_resolves(self):
        """
        Asserts the community general view (community) is resolved from
        'communities'.
        """
        path = reverse('communities')
        self.assertEqual(resolve(path).func, community_general)

    def test_community_specific_resolves(self):
        """
        Asserts specific community views (community) resolve
        from 'community' with slug arguments generated from the
        community name.
        """
        path = reverse('community', args=['testgenre-community'])
        self.assertEqual(resolve(path).func, community)

    def test_forum_detail_resolves(self):
        """
        Asserts the genre-specific forum details (forum_detail) resolve
        from 'forum-detail' with slug arguments generated from the
        forum name.
        """
        path = reverse('forum_detail', args=['forum-name'])
        self.assertEqual(resolve(path).func, forum_detail)

    def test_author_registration_resolves(self):
        """
        Asserts the author registration view (create_author) is resolved from
        'create_author'.
        """
        path = reverse('create_author')
        self.assertEqual(resolve(path).func, create_author)

    def test_book_registration_resolves(self):
        """
        Asserts the book upload/registration view (upload_book) is resolved
        from 'upload_book'.
        """
        path = reverse('upload_book')
        self.assertEqual(resolve(path).func, upload_book)

    def test_delete_message_from_forum_resolves(self):
        """
        Asserts the view for deleting forum messages (delete_message) resolves
        from 'delete_message' with arguments of slug: forum name and
        int: message id.
        """
        path = reverse('delete_message', args=['forum-name', 4])
        self.assertEqual(resolve(path).func, delete_message)
