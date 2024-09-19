from django.test import TestCase
from .forms import *


class TestOrderForm(TestCase):
    """
    A class for testing the Order Form associated with the Checkout app.
    This form allows users to place orders by specifying their billing address.

    Methods:
    def test_order_form_name_is_required():
        Asserts the order form is invalid without a full_name value.
        Asserts the error raised as a result of the empty value stems
        from the "full_name" key.
        Asserts the error raises matches the expected error.


    def test_order_form_email_is_required():
        Asserts the order form is invalid without an email value.
        Asserts the error raised as a result of the empty value stems
        from the "email" key.
        Asserts the error raises matches the expected error.


    def test_order_form_email_format_is_correct():
        Asserts the contact form is invalid if the email value is of
        an incorrect format.
        Asserts the error raised as a result of the incorrectly-formatted
        value stems from the "email" key.
        Asserts the error raises matches the expected error.


    def test_order_form_phone_number_is_required():
        Asserts the order form is invalid without a phone_number value.
        Asserts the error raised as a result of the empty value stems
        from the "phone_number" key.
        Asserts the error raises matches the expected error.


    def test_order_form_street_1_is_required():
        Asserts the contact form is invalid without a street_1 value.
        Asserts the error raised as a result of the empty value stems
        from the "street_1" key.
        Asserts the error raises matches the expected error.


    def test_order_form_street_2_is_not_required():
        Asserts the contact form is valid if there is no
        street_2 value provided by the user at checkout.


    def test_order_form_town_city_is_required():
        Asserts the contact form is invalid without a town_city value.
        Asserts the error raised as a result of the empty value stems
        from the "town_city" key.
        Asserts the error raises matches the expected error.


    def test_order_form_postcode_is_not_required():
        Asserts the contact form is valid if there is no
        postcode value provided by the user at checkout.


    def test_order_form_county_is_not_required():
        Asserts the contact form is valid if there is no
        county value provided by the user at checkout.


    def test_order_form_country_is_required():
        Asserts the contact form is invalid without a country value.
        Asserts the error raised as a result of the empty value stems
        from the "country" key.
        Asserts the error raises matches the expected error.


    def test_order_form_country_must_be_predefined():
        Asserts the contact form is invalid with an incorrect value.
        Asserts the error raised as a result of the incorrect value stems
        from the "country" key.
        Asserts the error raises matches the expected error.


    def test_fully_and_correctly_filled_form_is_valid():
        Asserts an order form instance that is full and
        correctly filled out is valid.


    def test_partially_but_correctly_filled_form_is_valid():
        Asserts an order form instance that is partially but
        correctly filled out is valid.
    """
    def test_order_form_name_is_required(self):
        """
        Asserts the order form is invalid without a full_name value.
        Asserts the error raised as a result of the empty value stems
        from the "full_name" key.
        Asserts the error raises matches the expected error.
        """
        order_form = OrderForm({
            "full_name": "",
            "email": "tester@email.com",
            "phone_number": "123 456 7890",
            "street_1": "Street Address 1",
            "street_2": "Street Address 2",
            "town_city": "Town",
            "postcode": "12345",
            "county": "County",
            "country": "IE"
        })
        self.assertFalse(order_form.is_valid())
        self.assertIn("full_name", order_form.errors.keys())
        self.assertEqual(
            order_form.errors["full_name"][0],
            "This field is required."
        )

    def test_order_form_email_is_required(self):
        """
        Asserts the order form is invalid without an email value.
        Asserts the error raised as a result of the empty value stems
        from the "email" key.
        Asserts the error raises matches the expected error.
        """
        order_form = OrderForm({
            "full_name": "Tester Tester",
            "email": "",
            "phone_number": "123 456 7890",
            "street_1": "Street Address 1",
            "street_2": "Street Address 2",
            "town_city": "Town",
            "postcode": "12345",
            "county": "County",
            "country": "IE"
        })
        self.assertFalse(order_form.is_valid())
        self.assertIn("email", order_form.errors.keys())
        self.assertEqual(
            order_form.errors["email"][0],
            "This field is required."
        )

    def test_order_form_email_format_is_correct(self):
        """
        Asserts the contact form is invalid if the email value is of
        an incorrect format.
        Asserts the error raised as a result of the incorrectly-formatted
        value stems from the "email" key.
        Asserts the error raises matches the expected error.
        """
        order_form = OrderForm({
            "full_name": "Tester Tester",
            "email": "123gh",
            "phone_number": "123 456 7890",
            "street_1": "Street Address 1",
            "street_2": "Street Address 2",
            "town_city": "Town",
            "postcode": "12345",
            "county": "County",
            "country": "IE"
        })
        self.assertFalse(order_form.is_valid())
        self.assertIn("email", order_form.errors.keys())
        self.assertEqual(
            order_form.errors["email"][0],
            "Enter a valid email address."
        )

    def test_order_form_phone_number_is_required(self):
        """
        Asserts the order form is invalid without a phone_number value.
        Asserts the error raised as a result of the empty value stems
        from the "phone_number" key.
        Asserts the error raises matches the expected error.
        """
        order_form = OrderForm({
            "full_name": "Tester Tester",
            "email": "tester@email.com",
            "phone_number": "",
            "street_1": "Street Address 1",
            "street_2": "Street Address 2",
            "town_city": "Town",
            "postcode": "12345",
            "county": "County",
            "country": "IE"
        })
        self.assertFalse(order_form.is_valid())
        self.assertIn("phone_number", order_form.errors.keys())
        self.assertEqual(
            order_form.errors["phone_number"][0],
            "This field is required."
        )

    def test_order_form_street_1_is_required(self):
        """
        Asserts the contact form is invalid without a street_1 value.
        Asserts the error raised as a result of the empty value stems
        from the "street_1" key.
        Asserts the error raises matches the expected error.
        """
        order_form = OrderForm({
            "full_name": "Tester Tester",
            "email": "tester@email.com",
            "phone_number": "123 456 7890",
            "street_1": "",
            "street_2": "Street Address 2",
            "town_city": "Town",
            "postcode": "12345",
            "county": "County",
            "country": "IE"
        })
        self.assertFalse(order_form.is_valid())
        self.assertIn("street_1", order_form.errors.keys())
        self.assertEqual(
            order_form.errors["street_1"][0],
            "This field is required."
        )

    def test_order_form_street_2_is_not_required(self):
        """
        Asserts the contact form is valid if there is no
        street_2 value provided by the user at checkout.
        """
        order_form = OrderForm({
            "full_name": "Tester Tester",
            "email": "tester@email.com",
            "phone_number": "123 456 7890",
            "street_1": "Street Address 1",
            "street_2": "",
            "town_city": "Town",
            "postcode": "12345",
            "county": "County",
            "country": "IE"
        })
        self.assertTrue(order_form.is_valid())

    def test_order_form_town_city_is_required(self):
        """
        Asserts the contact form is invalid without a town_city value.
        Asserts the error raised as a result of the empty value stems
        from the "town_city" key.
        Asserts the error raises matches the expected error.
        """
        order_form = OrderForm({
            "full_name": "Tester Tester",
            "email": "tester@email.com",
            "phone_number": "123 456 7890",
            "street_1": "Street Address 1",
            "street_2": "Street Address 2",
            "town_city": "",
            "postcode": "12345",
            "county": "County",
            "country": "IE"
        })
        self.assertFalse(order_form.is_valid())
        self.assertIn("town_city", order_form.errors.keys())
        self.assertEqual(
            order_form.errors["town_city"][0],
            "This field is required."
        )

    def test_order_form_postcode_is_not_required(self):
        """
        Asserts the contact form is valid if there is no
        postcode value provided by the user at checkout.
        """
        order_form = OrderForm({
            "full_name": "Tester Tester",
            "email": "tester@email.com",
            "phone_number": "123 456 7890",
            "street_1": "Street Address 1",
            "street_2": "Street Address 2",
            "town_city": "Town",
            "postcode": "",
            "county": "County",
            "country": "IE"
        })
        self.assertTrue(order_form.is_valid())

    def test_order_form_county_is_not_required(self):
        """
        Asserts the contact form is valid if there is no
        county value provided by the user at checkout.
        """
        order_form = OrderForm({
            "full_name": "Tester Tester",
            "email": "tester@email.com",
            "phone_number": "123 456 7890",
            "street_1": "Street Address 1",
            "street_2": "Street Address 2",
            "town_city": "Town",
            "postcode": "12345",
            "county": "",
            "country": "IE"
        })
        self.assertTrue(order_form.is_valid())

    def test_order_form_country_is_required(self):
        """
        Asserts the contact form is invalid without a country value.
        Asserts the error raised as a result of the empty value stems
        from the "country" key.
        Asserts the error raises matches the expected error.
        """
        order_form = OrderForm({
            "full_name": "Tester Tester",
            "email": "tester@email.com",
            "phone_number": "123 456 7890",
            "street_1": "Street Address 1",
            "street_2": "Street Address 2",
            "town_city": "Town",
            "postcode": "12345",
            "county": "County",
            "country": ""
        })
        self.assertFalse(order_form.is_valid())
        self.assertIn("country", order_form.errors.keys())
        self.assertEqual(
            order_form.errors["country"][0],
            "This field is required."
        )

    def test_order_form_country_must_be_predefined(self):
        """
        Asserts the contact form is invalid with an incorrect value.
        Asserts the error raised as a result of the incorrect value stems
        from the "country" key.
        Asserts the error raises matches the expected error.
        """
        order_form = OrderForm({
            "full_name": "Tester Tester",
            "email": "tester@email.com",
            "phone_number": "123 456 7890",
            "street_1": "Street Address 1",
            "street_2": "Street Address 2",
            "town_city": "Town",
            "postcode": "12345",
            "county": "County",
            "country": "KK"
        })
        self.assertFalse(order_form.is_valid())
        self.assertIn("country", order_form.errors.keys())
        self.assertEqual(
            order_form.errors["country"][0],
            "Select a valid choice. KK is not one of the available choices."
        )

    def test_fully_and_correctly_filled_form_is_valid(self):
        """
        Asserts an order form instance that is full and
        correctly filled out is valid.
        """
        order_form = OrderForm({
            "full_name": "Tester Tester",
            "email": "tester@email.com",
            "phone_number": "123 456 7890",
            "street_1": "Street Address 1",
            "street_2": "Street Address 2",
            "town_city": "Town",
            "postcode": "12345",
            "county": "County",
            "country": "IE"
        })
        self.assertTrue(order_form.is_valid())

    def test_partially_but_correctly_filled_form_is_valid(self):
        """
        Asserts an order form instance that is partially but
        correctly filled out is valid.
        """
        order_form = OrderForm({
            "full_name": "Tester Tester",
            "email": "tester@email.com",
            "phone_number": "123 456 7890",
            "street_1": "Street Address 1",
            "street_2": "",
            "town_city": "Town",
            "postcode": "",
            "county": "",
            "country": "IE"
        })
        self.assertTrue(order_form.is_valid())
