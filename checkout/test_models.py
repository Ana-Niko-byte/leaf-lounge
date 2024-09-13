from django.shortcuts import get_object_or_404
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

# Signal triggering user_profile creation after user login.
from reader.signals import create_or_save_profile

from .models import *
from library.models import Author, Genre, Book
from decimal import Decimal


class TestCheckoutModels(TestCase):
    """
    A class for testing the order and booklineitem models in the checkout app.
    Testing includes asserting equal values to those in the model setup, save
    method testing, and format validation for timezone objects and slugs.

    Methods:
    def setUp():
        REGISTRATION:
        Simulates user registration to allow for the creation of a user
        profile.

        USER PROFILE & AUTHOR PROFILE:
        Retrieves the user profile automatically created following successful
        user registration. This is handled via
        reader.signals.create_or_save_profile.
        Simulates the creation of an author profile and assigns the relevant
        user profile to the author.user_profile field.

        GENRE & COMMUNITY:
        Simulates the creation of a genre.

        BOOK:
        Simulates the creation of a book with relevant relationships to the
        author and genre models.

        ORDER & BOOKLINEITEM:
        Simulates the creation of an order with no order number.
        Simulates the creation of a booklineitem, with relevant relationships
        to the order and book models. These models in turn depend on the
        genre, user profile, and author models.

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
        Asserts a ValidationError is raised if the full_name field is empty,
        or has no value, or is longer than 50 characters.

        Asserts the order's associated email matches the model's setup.
        Asserts a ValidationError is raised if the email field is empty,
        or has no value, or is of an unexpected format.

        Asserts the order's associated phone_number matches the model's setup.
        Asserts a ValidationError is raised if the phone_number field is empty,
        or has no value, or is longer than 20 characters.

        Asserts the order's associated country matches the model's setup.
        Asserts a ValidationError is raised if the country field is empty,
        or has no value, or is of an unexpected format.

        Asserts the order's associated postcode matches the model's setup.
        Asserts a ValidationError is raised if the postcode is of an unexpected
        format.

        Asserts the order's associated town_city matches the model's setup.
        Asserts a ValidationError is raised if the town_city field is empty,
        or has no value, or is longer than 40 characters.

        Asserts the order's associated street_1 matches the model's setup.
        Asserts a ValidationError is raised if the street_1 field is empty,
        or has no value, or is longer than 80 characters.

        Asserts the order's associated street_2 matches the model's setup.
        Asserts a ValidationError is raised if the street_2 field is empty,
        or has no value, or is longer than 80 characters.

        Asserts the order's associated county matches the model's setup.
        Asserts a ValidationError is raised if the county is longer than 80
        characters.


    def test_order_creation_and_decimal_fields():
        Retrieves the appropriate order instance for testing.
        Asserts the order's __str__() returns the expected string for the
        appropriate order instance.

        Asserts the order's associated date matches the current date.
        Asserts a ValidationError is raised if the date field is empty or
        has no value.

        Asserts the order's delivery_cost field is a Decimal format that
        matches the model's setup value. This valus is preset in the app
        settings.
        Asserts the delivery_cost cannot be null or empty.
        Asserts a ValidationError is raised if the delivery_cost is over 6
        decimals, i.e., a book's value is raised too high.

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


    def test_booklineitem_creation():
        Retrieves the appropriate booklineitem instance for testing.
        Asserts the booklineitem's __str__() returns the expected string for
        the appropriate booklineitem instance.

        Asserts the booklineitem's order's user matches the appropriate user.
        Asserts the booklineitem's book matches the appropriate book.
        Asserts the booklineitem book type matches the model's set up and
        raises a ValidationError if there is no type or the type value is
        empty.

        Asserts the booklineitem quantity matches the model's set up and raises
        a ValidationError is there is no quantity, the quantity is under the
        minimum value of 1, or over the maximum value of 99.

        Asserts the booklineitem book_order_cost is calculated and saved
        correctly.
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
        Simulates the creation of an author profile and assigns the relevant
        user profile to the author.user_profile field.

        GENRE & COMMUNITY:
        Simulates the creation of a genre.

        BOOK:
        Simulates the creation of a book with relevant relationships to the
        author and genre models.

        ORDER & BOOKLINEITEM:
        Simulates the creation of an order with no order number.
        Simulates the creation of a booklineitem, with relevant relationships
        to the order and book models. These models in turn depend on the
        genre, user profile, and author models.

        Saves the relevant models to the test sqlite3 database.
        """
        self.client = Client()
        self.user = User(username="ananiko")
        self.user.set_password("modeltesting")
        self.user.save()

        self.user_profile = get_object_or_404(UserProfile, user=self.user)
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
            price=14.99
        )
        self.book.save()

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
            original_basket="test",
            stripe_pid="teststripepid"
        )
        self.order.save()

        self.booklineitem = BookLineItem(
            order=self.order,
            book=self.book,
            type="Softcover",
            quantity=2
        )
        self.booklineitem.save()

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
        Asserts a ValidationError is raised if the full_name field is empty,
        or has no value, or is longer than 50 characters.

        Asserts the order's associated email matches the model's setup.
        Asserts a ValidationError is raised if the email field is empty,
        or has no value, or is of an unexpected format.

        Asserts the order's associated phone_number matches the model's setup.
        Asserts a ValidationError is raised if the phone_number field is empty,
        or has no value, or is longer than 20 characters.

        Asserts the order's associated country matches the model's setup.
        Asserts a ValidationError is raised if the country field is empty,
        or has no value, or is of an unexpected format.

        Asserts the order's associated postcode matches the model's setup.
        Asserts a ValidationError is raised if the postcode is of an unexpected
        format.

        Asserts the order's associated town_city matches the model's setup.
        Asserts a ValidationError is raised if the town_city field is empty,
        or has no value, or is longer than 40 characters.

        Asserts the order's associated street_1 matches the model's setup.
        Asserts a ValidationError is raised if the street_1 field is empty,
        or has no value, or is longer than 80 characters.

        Asserts the order's associated street_2 matches the model's setup.
        Asserts a ValidationError is raised if the street_2 field is empty,
        or has no value, or is longer than 80 characters.

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
        Asserts a ValidationError is raised if the date field is empty or
        has no value.

        Asserts the order's delivery_cost field is a Decimal format that
        matches the model's setup value. This valus is preset in the app
        settings.
        Asserts the delivery_cost cannot be null or empty.
        Asserts a ValidationError is raised if the delivery_cost is over 6
        decimals, i.e., a book's value is raised too high.

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

        self.assertEqual(order.delivery_cost, Decimal("3.00"))
        with self.assertRaises(ValidationError):
            order.delivery_cost = None
            order.full_clean()
        with self.assertRaises(ValidationError):
            order.delivery_cost = 14011.99
            order.full_clean()

        self.assertEqual(order.order_total, Decimal("29.98"))
        with self.assertRaises(ValidationError):
            order.order_total = None
            order.full_clean()
        with self.assertRaises(ValidationError):
            order.order_total = 14046543611.99
            order.full_clean()
        with self.assertRaises(ValidationError):
            order.order_total = Decimal("-1.24")
            order.full_clean()

        self.assertEqual(order.grand_total, Decimal("32.98"))
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

    def test_booklineitem_creation(self):
        """
        Retrieves the appropriate booklineitem instance for testing.
        Asserts the booklineitem's __str__() returns the expected string for
        the appropriate booklineitem instance.

        Asserts the booklineitem's order's user matches the appropriate user.
        Asserts the booklineitem's book matches the appropriate book.
        Asserts the booklineitem book type matches the model's set up and
        raises a ValidationError if there is no type or the type value is
        empty.

        Asserts the booklineitem quantity matches the model's set up and raises
        a ValidationError is there is no quantity, the quantity is under the
        minimum value of 1, or over the maximum value of 99.

        Asserts the booklineitem book_order_cost is calculated and saved
        correctly.
        """
        booklineitem = get_object_or_404(BookLineItem, order=self.order)
        # Line breaks PEP8 standards but no way of shortening.
        self.assertEqual(
            booklineitem.__str__(),
            f"ISBN : {booklineitem.book.isbn}, order: {booklineitem.order.order_number}"
        )

        self.assertEqual(
            booklineitem.order.user_profile.user.username,
            "ananiko"
        )
        self.assertEqual(booklineitem.book.title, "How to Test Django Models")

        self.assertEqual(booklineitem.type, "Softcover")
        with self.assertRaises(ValidationError):
            booklineitem.type = None
            booklineitem.full_clean()
        with self.assertRaises(ValidationError):
            booklineitem.type = ""
            booklineitem.full_clean()

        self.assertEqual(booklineitem.quantity, 2)
        with self.assertRaises(ValidationError):
            self.booklineitem.quantity = None
            self.booklineitem.full_clean()
        with self.assertRaises(ValidationError):
            self.booklineitem.quantity = -3
            self.booklineitem.full_clean()
        with self.assertRaises(ValidationError):
            self.booklineitem.quantity = 100
            self.booklineitem.full_clean()

        self.assertEqual(
            booklineitem.book_order_cost, Decimal(
                f"{self.book.price}"
            ) * booklineitem.quantity
        )
