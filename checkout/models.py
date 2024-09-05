from django.db import models
from django.db.models import Sum
from django.conf import settings
from django_countries.fields import CountryField

from library.models import Book
from reader.models import UserProfile

import uuid


class Order(models.Model):
    """
    Represents a user's book Order. Orders are placed via the checkout page.
    Order histories can be viewed under the 'My Profile' tab.

    Fields:
    order_number : CharField - the auto-generated uuid order number.
    user_profile : FK : UserProfile - the profile to which the order belongs.
    full_name : CharField - the full name associated with the order.
    email : EmailField - the email associated with the order.
    phone_number: CharField - the phone number associated with the order.
    country : CharField - the country to which the order is to be posted.
    postcode : CharField - the postcode associated with the order address.
    town_city: CharField - the town/city to which the order is to be posted.
    street_1 : CharField - the first address line on the order.
    street_2 : CharField - the second address line on the order.
    county : CharField - the county to which the order is to be posted.
    date : DateTimeField - the time and date the order was placed.
    delivery_cost : DecimalField - the delivery cost associated with the order.
    order_total : DecimalField - the total associated with the price/book
    and quantity.
    grand_total : DecimalField - order_total + delivery_cost.
    original_basket : TextField - the order basket's original basket.
    stripe_pid : CharField - the Stripe order pid.

    Methods:
    def _generate_uuid_order_number():
        Generates a random, unique order number using UUID.

    def save():
        try:
            Asserts whether an order number exists.
            Saves a new order number from def _generate_uuid_order_number().
        except Order.DoesNotExist:
            Catches the DoesNotExist error and saves the model as a new
            instance.

    def update_order_total():
        Updates 'order_total', 'delivery_cost', and 'grand_total' based on
        order_total and quantity.
        Asserts whether the 'order_total' is above the FREE_DELIVERY_THRESHOLD,
        as defined in settings.py.
        If above, assigns 0 to 'delivery_cost'.
        If below, assigns 10% of 'order_total' value as 'delivery_cost'.
        Assigns 'grand_total' the sum of 'order_total' + 'delivery_cost'.

    def __str__() -> int : order number.
    """

    order_number = models.CharField(
        max_length=32,
        null=False,
        editable=False
    )
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    full_name = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
    email = models.EmailField(
        max_length=254,
        null=False,
        blank=False
    )
    phone_number = models.CharField(
        max_length=20,
        null=False,
        blank=False
    )
    country = CountryField(
        blank_label='Country *',
        null=False,
        blank=False
    )
    postcode = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    town_city = models.CharField(
        max_length=40,
        null=False,
        blank=False
    )
    street_1 = models.CharField(
        max_length=80,
        null=False,
        blank=False
    )
    street_2 = models.CharField(
        max_length=80,
        null=True,
        blank=True
    )
    county = models.CharField(
        max_length=80,
        null=True,
        blank=True
    )
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        default=0
    )
    order_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        default=0
    )
    grand_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        default=0
    )
    original_basket = models.TextField(
        null=False,
        blank=False,
        default=''
    )
    stripe_pid = models.CharField(
        max_length=254,
        null=False,
        blank=False,
        default=''
    )

    def _generate_uuid_order_number(self):
        """
        Generates a random, unique order number using UUID.
        """
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """
        Assigns an order number to each Order if one is not already assigned.
        """
        try:
            if not self.order_number:
                self.order_number = self._generate_uuid_order_number()
            super(Order, self).save(*args, **kwargs)
        except Order.DoesNotExist:
            super(Order, self).save(*args, **kwargs)

    def update_order_total(self):
        """
        Updates the 'order_total', 'delivery_cost', and 'grand_total' for each
        order and saves the instance.
        """
        SDT = settings.STANDARD_DELIVERY_PERCENTAGE
        FDT = settings.FREE_DELIVERY_THRESHOLD
        self.order_total = self.booklineitem.aggregate(
            Sum(
                'book_order_cost'
                ))['book_order_cost__sum'] or 0

        if self.order_total < FDT:
            self.delivery_cost = self.order_total * SDT / 100
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()
        self.refresh_from_db()

    def __str__(self):
        """
        Returns -> int : order number.
        """
        return self.order_number


class BookLineItem(models.Model):
    """
    Represents a book lineitem for each book inside an order.

    Fields:
    order : FK : Order - the book order.
    book : FK : Book - the book instance that was ordered.
    type : CharField - the book cover type.
    quantity : IntegerField - the quantity that was ordered.
    book_order_cost : DecimalField - the total cost for the book order.

    Methods:
    def save():
        Assigns the total lineitem cost based on price/unit and quantity if not
        already assigned.

    def __str__() -> str : 'ISBN: (book ISBN), order: (order number uuid)'.
    """
    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='booklineitem'
    )
    book = models.ForeignKey(
        Book,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='bookdetails'
    )
    type = models.CharField(
        max_length=9,
        null=False,
        blank=False,
    )
    quantity = models.IntegerField(
        null=False,
        blank=False,
        default=0
    )
    book_order_cost = models.DecimalField(
        max_digits=5,
        null=False,
        blank=False,
        decimal_places=2,
        editable=False
    )

    def save(self, *args, **kwargs):
        """
        Assigns the total lineitem cost based on price/unit and quantity
        if not already assigned.
        """
        # Line breaks PEP8 standards but no way to shorten it without renaming.
        if not self.book_order_cost or self.book_order_cost != self.book.price * self.quantity:
            self.book_order_cost = self.book.price * self.quantity
        super(BookLineItem, self).save(*args, **kwargs)

    def __str__(self):
        """
        Returns -> str : 'ISBN: (book ISBN), order: (order number uuid)'.
        """
        return f'ISBN : {self.book.isbn}, order: {self.order.order_number}'
