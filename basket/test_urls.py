from django.test import TestCase
from django.urls import reverse, resolve
from .views import *


class TestBasketURLs(TestCase):
    """
    A class for testing URLs associated with the basket app.
    This class tests urls resolve from their FBVs and that certain
    views are allowed to handle DELETE requests.

    Methods:
    def test_basket_resolves():
        Reverses the URL name and checks if it returns the correct FBV of
        basket.

        Asserts the basket view (basket) is resolved from 'basket'.


    def test_add_to_basket_resolves():
        Reverses the URL name with arguments [int:book_id] and checks if it
        returns the correct FBV of add_basket.

        Asserts the view for adding items to basket (add_basket) is resolved
        from 'add_to_basket' with an int argument.


    def test_update_basket_resolves():
        Reverses the URL name with arguments [int:book_id] and checks if it
        returns the correct FBV of amend_basket.

        Asserts the view for updating items in basket (amend_basket) is
        resolved from 'update_basket' with an int argument.


    def test_delete_from_basket_resolves():
        Reverses the URL name with arguments [slug, int:book_id] and checks if
        it returns the correct FBV of delete_basket.

        Asserts the view for deleting items from basket (delete_basket) is
        resolved from 'delete_basket' with an int argument.

        Asserts the view is allowed to handle DELETE requests.
    """

    def test_basket_resolves(self):
        """
        Asserts the basket view (basket) is resolved from 'basket'.
        """
        path = reverse('basket')
        self.assertEqual(resolve(path).func, basket)

    def test_add_to_basket_resolves(self):
        """
        Asserts the view for adding items to basket (add_basket) is resolved
        from 'add_to_basket' with an int argument.
        """
        path = reverse('add_to_basket', args=[6])
        self.assertEqual(resolve(path).func, add_basket)

    def test_update_basket_resolves(self):
        """
        Asserts the view for updating items in basket (amend_basket) is
        resolved from 'update_basket' with an int argument.
        """
        path = reverse('update_basket', args=[4])
        self.assertEqual(resolve(path).func, amend_basket)

    def test_delete_from_basket_resolves(self):
        """
        Asserts the view for deleting items from basket (delete_basket) is
        resolved from 'delete_basket' with an int argument.

        Asserts the view is allowed to handle DELETE requests.
        """
        path = reverse('delete_basket', args=[3])
        self.assertEqual(resolve(path).func, delete_basket)

        res = self.client.delete(path)
        self.assertEqual(res.status_code, 200)
