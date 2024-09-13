from django.shortcuts import get_object_or_404
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

# Signal triggering user_profile creation after user login.
from reader.signals import create_or_save_profile

from .models import *
from decimal import Decimal


class TestCheckoutModels(TestCase):
    """

    Methods:
    def setUp():
        REGISTRATION:
        Simulates user registration to allow for the creation of a user
        profile.

        USER PROFILE & AUTHOR PROFILE:
        Retrieves the user profile automatically created following successful
        user registration. This is handled via
        reader.signals.create_or_save_profile.

        ORDER:
        Simulates the creation of an order with no order number.

        Saves the relevant models to the test sqlite3 database.

    def test_order_creation_and_string_fields():
        Retrieves the appropriate order instance for testing.
        Asserts the order's __str__() returns the expected string for the
        appropriate order instance.

        Asserts order associated user profile matches the expected user
        profile.
        Asserts the order's user's username matches the expected value.

        Asserts the order's order number is not empty or None. This ensures
        that the model was saved and an order number was automatically
        generated and assigned.

        Asserts the order's associated user's full name matches the model's
        setup.
        Asserts a ValidationError is raised if the full_name field is empty.
        Asserts a ValidationError is raised if there is no full_name value.
        Asserts a ValidationError is raised if the full_name is longer than
        50 characters.

        Asserts the order's associated email matches the model's setup.
        Asserts a ValidationError is raised if the email field is empty.
        Asserts a ValidationError is raised if there is no email value.
        Asserts a ValidationError is raised if the email is of an unexpected
        format.

        Asserts the order's associated phone_number matches the model's setup.
        Asserts a ValidationError is raised if the phone_number field is empty.
        Asserts a ValidationError is raised if there is no phone_number value.
        Asserts a ValidationError is raised if the phone_number is longer than
        20 characters.

        Asserts the order's associated country matches the model's setup.
        Asserts a ValidationError is raised if the country field is empty.
        Asserts a ValidationError is raised if there is no country value.
        Asserts a ValidationError is raised if the country is of an unexpected
        format.

        Asserts the order's associated postcode matches the model's setup.
        Asserts a ValidationError is raised if the postcode is of an unexpected
        format.

        Asserts the order's associated town_city matches the model's setup.
        Asserts a ValidationError is raised if the town_city field is empty.
        Asserts a ValidationError is raised if there is no town_city value.
        Asserts a ValidationError is raised if the town_city is longer than 40
        characters.

        Asserts the order's associated street_1 matches the model's setup.
        Asserts a ValidationError is raised if the street_1 field is empty.
        Asserts a ValidationError is raised if there is no street_1 value.
        Asserts a ValidationError is raised if the street_1 is longer than 80
        characters.

        Asserts the order's associated street_2 matches the model's setup.
        Asserts a ValidationError is raised if the street_2 field is empty.
        Asserts a ValidationError is raised if there is no street_2 value.
        Asserts a ValidationError is raised if the street_2 is longer than 80
        characters.

        Asserts the order's associated county matches the model's setup.
        Asserts a ValidationError is raised if the county is longer than 80
        characters.

    def test_order_creation_and_decimal_fields():
        Retrieves the appropriate order instance for testing.
        Asserts the order's __str__() returns the expected string for the
        appropriate order instance.

        Asserts the order's associated date matches the current date.
        Asserts a ValidationError is raised if the date field is empty.
        Asserts a ValidationError is raised if there is no date value.

        Asserts the order's delivery_cost field is a Decimal format that
        matches the model's setup value.
        Asserts the delivery_cost cannot be null or empty.
        Asserts a ValidationError is raised if the delivery_cost is over 6
        decimals, i.e., a book's value is raised too high, or is below 0.

        Asserts the order's order_total field is a Decimal format that matches
        the model's setup value.
        Asserts the order_total cannot be null or empty.
        Asserts a ValidationError is raised if the order_total is over 10
        decimals, i.e., the order_total is raised too high, or is below 0.

        Asserts the order's grand_total field is a Decimal format that matches
        the model's setup value.
        Asserts the grand_total cannot be null or empty.
        Asserts a ValidationError is raised if the grand_total is over 10
        decimals, i.e., the grand_total is raised too high, or is below 0.

        Asserts the order's original basket identifier matches the model's
        setup value.
        Asserts there must be an original_basket value.

        Asserts the order's associated stripe_pid matches the models's setup
        value.
        Asserts a ValidationError is raised if there is no stripe_pid or it is
        empty.
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

        ORDER:
        Simulates the creation of an order with no order number.

        Saves the relevant models to the test sqlite3 database.
        """
        self.client = Client()
        self.user = User(username="ananiko")
        self.user.set_password("modeltesting")
        self.user.save()

        self.user_profile = get_object_or_404(UserProfile, user=self.user)
        # self.order_number = uuid.uuid4().hex.upper()

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
            delivery_cost=14.99,
            order_total=17.01,
            grand_total=17.01,
            original_basket="test",
            stripe_pid="teststripepid"
        )
        self.order.save()

    def test_order_creation_and_string_fields(self):
        """
        Retrieves the appropriate order instance for testing.
        Asserts the order's __str__() returns the expected string for the
        appropriate order instance.

        Asserts order associated user profile matches the expected user
        profile.
        Asserts the order's user's username matches the expected value.

        Asserts the order's order number is not empty or None. This ensures
        that the model was saved and an order number was automatically
        generated and assigned.

        Asserts the order's associated user's full name matches the model's
        setup.
        Asserts a ValidationError is raised if the full_name field is empty.
        Asserts a ValidationError is raised if there is no full_name value.
        Asserts a ValidationError is raised if the full_name is longer than
        50 characters.

        Asserts the order's associated email matches the model's setup.
        Asserts a ValidationError is raised if the email field is empty.
        Asserts a ValidationError is raised if there is no email value.
        Asserts a ValidationError is raised if the email is of an unexpected
        format.

        Asserts the order's associated phone_number matches the model's setup.
        Asserts a ValidationError is raised if the phone_number field is empty.
        Asserts a ValidationError is raised if there is no phone_number value.
        Asserts a ValidationError is raised if the phone_number is longer than
        20 characters.

        Asserts the order's associated country matches the model's setup.
        Asserts a ValidationError is raised if the country field is empty.
        Asserts a ValidationError is raised if there is no country value.
        Asserts a ValidationError is raised if the country is of an unexpected
        format.

        Asserts the order's associated postcode matches the model's setup.
        Asserts a ValidationError is raised if the postcode is of an unexpected
        format.

        Asserts the order's associated town_city matches the model's setup.
        Asserts a ValidationError is raised if the town_city field is empty.
        Asserts a ValidationError is raised if there is no town_city value.
        Asserts a ValidationError is raised if the town_city is longer than 40
        characters.

        Asserts the order's associated street_1 matches the model's setup.
        Asserts a ValidationError is raised if the street_1 field is empty.
        Asserts a ValidationError is raised if there is no street_1 value.
        Asserts a ValidationError is raised if the street_1 is longer than 80
        characters.

        Asserts the order's associated street_2 matches the model's setup.
        Asserts a ValidationError is raised if the street_2 field is empty.
        Asserts a ValidationError is raised if there is no street_2 value.
        Asserts a ValidationError is raised if the street_2 is longer than 80
        characters.

        Asserts the order's associated county matches the model's setup.
        Asserts a ValidationError is raised if the county is longer than 80
        characters.
        """
        order = get_object_or_404(Order, user_profile=self.user_profile)
        self.assertEqual(order.__str__(), f"{order.order_number}")

        self.assertEqual(order.user_profile, self.user_profile)
        self.assertEqual(order.user_profile.user.username, "ananiko")

        self.assertIsNotNone(order.order_number)

        self.assertEqual(order.full_name, "Firstname Lastname")
        with self.assertRaises(ValidationError):
            order.full_name = ""
            order.full_clean()
        with self.assertRaises(ValidationError):
            order.full_name = None
            order.full_clean()
        with self.assertRaises(ValidationError):
            order.full_name = """zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
                zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"""
            order.full_clean()

        self.assertEqual(order.email, "test@gmail.com")
        with self.assertRaises(ValidationError):
            order.email = ""
            order.full_clean()
        with self.assertRaises(ValidationError):
            order.email = None
            order.full_clean()
        with self.assertRaises(ValidationError):
            order.email = """zzzzzzzzzzzzzz"""
            order.full_clean()

        self.assertEqual(order.phone_number, "1234567890")
        with self.assertRaises(ValidationError):
            order.phone_number = ""
            order.full_clean()
        with self.assertRaises(ValidationError):
            order.phone_number = None
            order.full_clean()
        with self.assertRaises(ValidationError):
            order.phone_number = """123456789012345678901"""
            order.full_clean()

        self.assertEqual(order.country, "IE")
        with self.assertRaises(ValidationError):
            order.country = ""
            order.full_clean()
        with self.assertRaises(ValidationError):
            order.country = None
            order.full_clean()
        with self.assertRaises(ValidationError):
            order.country = """not a country"""
            order.full_clean()

        self.assertEqual(order.postcode, "V94 XXXX")
        with self.assertRaises(ValidationError):
            order.postcode = """not a real postcode"""
            order.full_clean()

        self.assertEqual(order.town_city, "Anywhere")
        with self.assertRaises(ValidationError):
            order.town_city = ""
            order.full_clean()
        with self.assertRaises(ValidationError):
            order.town_city = None
            order.full_clean()
        with self.assertRaises(ValidationError):
            order.town_city = """zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
                zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"""
            order.full_clean()

        self.assertEqual(order.street_1, "Street 1")
        with self.assertRaises(ValidationError):
            order.street_1 = ""
            order.full_clean()
        with self.assertRaises(ValidationError):
            order.street_1 = None
            order.full_clean()
        with self.assertRaises(ValidationError):
            order.street_1 = """zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
                zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"""
            order.full_clean()

        self.assertEqual(order.street_2, "Street 2")
        with self.assertRaises(ValidationError):
            order.street_2 = ""
            order.full_clean()
        with self.assertRaises(ValidationError):
            order.street_2 = None
            order.full_clean()
        with self.assertRaises(ValidationError):
            order.street_2 = """zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
                zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"""
            order.full_clean()

        self.assertEqual(order.county, "Anycounty")
        with self.assertRaises(ValidationError):
            order.county = """zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
                zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"""
            order.full_clean()

    def test_order_creation_and_decimal_fields(self):
        """
        Retrieves the appropriate order instance for testing.
        Asserts the order's __str__() returns the expected string for the
        appropriate order instance.

        Asserts the order's associated date matches the current date.
        Asserts a ValidationError is raised if the date field is empty.
        Asserts a ValidationError is raised if there is no date value.

        Asserts the order's delivery_cost field is a Decimal format that
        matches the model's setup value.
        Asserts the delivery_cost cannot be null or empty.
        Asserts a ValidationError is raised if the delivery_cost is over 6
        decimals, i.e., a book's value is raised too high, or is below 0.

        Asserts the order's order_total field is a Decimal format that matches
        the model's setup value.
        Asserts the order_total cannot be null or empty.
        Asserts a ValidationError is raised if the order_total is over 10
        decimals, i.e., the order_total is raised too high, or is below 0.

        Asserts the order's grand_total field is a Decimal format that matches
        the model's setup value.
        Asserts the grand_total cannot be null or empty.
        Asserts a ValidationError is raised if the grand_total is over 10
        decimals, i.e., the grand_total is raised too high, or is below 0.

        Asserts the order's original basket identifier matches the model's
        setup value.
        Asserts there must be an original_basket value.

        Asserts the order's associated stripe_pid matches the models's setup
        value.
        Asserts a ValidationError is raised if there is no stripe_pid or it is
        empty.
        """
        order = get_object_or_404(Order, user_profile=self.user_profile)
        self.assertEqual(order.__str__(), f"{order.order_number}")

        self.assertEqual(order.date.date(), timezone.now().date())
        with self.assertRaises(ValidationError):
            order.date = None
            order.full_clean()
        with self.assertRaises(ValidationError):
            order.date = ""
            order.full_clean()

        self.assertEqual(order.delivery_cost, Decimal("14.99"))
        with self.assertRaises(ValidationError):
            order.delivery_cost = None
            order.full_clean()
        with self.assertRaises(ValidationError):
            order.delivery_cost = 14011.99
            order.full_clean()
        with self.assertRaises(ValidationError):
            order.delivery_cost = Decimal("-1.24")
            order.full_clean()

        self.assertEqual(order.order_total, Decimal("17.01"))
        with self.assertRaises(ValidationError):
            order.order_total = None
            order.full_clean()
        with self.assertRaises(ValidationError):
            order.order_total = 14046543611.99
            order.full_clean()
        with self.assertRaises(ValidationError):
            order.order_total = Decimal("-1.24")
            order.full_clean()

        self.assertEqual(order.grand_total, Decimal("17.01"))
        with self.assertRaises(ValidationError):
            order.grand_total = None
            order.full_clean()
        with self.assertRaises(ValidationError):
            order.grand_total = 14046543611.99
            order.full_clean()
        with self.assertRaises(ValidationError):
            order.grand_total = Decimal("-1.24")
            order.full_clean()

        self.assertEqual(order.original_basket, "test")
        with self.assertRaises(ValidationError):
            order.original_basket = None
            order.full_clean()
        with self.assertRaises(ValidationError):
            order.original_basket = ""
            order.full_clean()

        self.assertEqual(order.stripe_pid, "teststripepid")
        with self.assertRaises(ValidationError):
            order.stripe_pid = None
            order.full_clean()
        with self.assertRaises(ValidationError):
            order.stripe_pid = ""
            order.full_clean()