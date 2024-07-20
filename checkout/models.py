from django.db import models
from django.db.models import Sum
from django.conf import settings

from library.models import Book

import uuid


class Order(models.Model):
    """
    """
    SDT = settings.STANDARD_DELIVERY_PERCENTAGE
    FDT = settings.FREE_DELIVERY_THRESHOLD

    order_number = models.CharField(
        max_length=32,
        null=False,
        editable=False
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
    country = models.CharField(
        max_length=40,
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

    def _generate_uuid_order_number(self):
        """
        Generate a random, unique order number using UUID.
        """
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """
        Assign an order number to each Order if one not assigned already.
        """
        if not self.order_number:
            self.order_number = self._generate_uuid_order_number()
        super(Order, self).save(*args, **kwargs)

    def update_order_total(self):
        """
        Updates 'order_total', 'delivery_cost', and 'grand_total'
        and saves the model.
        """
        self.order_total = self.booklineitem.aggregate(
            Sum(
                'book_order_cost'
                ))['book_order_cost__sum']
        if self.order_total < FDT:
            self.delivery_cost = self.order_total * SDT / 100
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def __str__(self):
        """
        returns (int) : order number.
        """
        return self.order_number


class BookLineItem(models.Model):
    """
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
        on_delete=models.CASCADE
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
        if not self.book_order_cost:
            self.book_order_cost = self.book.price * self.quantity
        super(BookLineItem, self).save(*args, **kwargs)

    def __str__(self):
        """
        returns (str) : 'ISBN: (book ISBN), order: (order number uuid)'.
        """

        return f'ISBN : {self.book.isbn}, order: {self.order.order_number}'
