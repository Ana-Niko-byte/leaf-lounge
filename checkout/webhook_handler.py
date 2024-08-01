from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from reader.models import UserProfile
from library.models import *
from .models import *

import json
import time
import logging
import stripe


class StripeWH_Handler():
    """
    A class for handling Stripe Webhooks.
    """
    def __init__(self, request):
        self.request = request
        # logging.basicConfig(level=logging.DEBUG)
        # does not log
        logging.critical("This should get logged.")

    def handle_event(self, event):
        """
        Handles generic/unknown/unexpected webhook events.
        """
        return HttpResponse(
            content=f'WH UNHANDLED: {event['type']}',
            status=200
        )

    def _send_email(self, order):
        """
        Sends a confirmation email to users following successful payment.

        Arguments:
        order : the user's order.
        """
        email = order.email
        subject = render_to_string(
            'checkout/confirmation_email/confirmation_email_subject.txt',
            {'book_order': order}
        )
        message = render_to_string(
            'checkout/confirmation_email/confirmation_email_body.txt',
            {'book_order': order}
        )
        print(email, subject, message)
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[f"{email}"],
            fail_silently=False,
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handles the payment_intent.succeeded webhook from Stripe.

        Arguments:
        event : JSON object : event data sent by Stripe with all details
        relating to the payment.
        """
        # Extracts main data from the intent payment object (dict).
        intent = event.data.object
        pid = intent.id

        basket = intent.metadata.basket
        save_info = intent.metadata.save_info

        stripe_charge = stripe.Charge.retrieve(intent.latest_charge)
        # Or intent['charges']['data'][0]['billing_details'] from ^^ dict.
        billing_details = stripe_charge.billing_details
        shipping_details = intent.shipping
        grand_total = round(stripe_charge.amount / 100, 2)

        # Update Profile Information.
        # Except it does not update so look over code later.
        u_prof = None
        username = intent.metadata.username
        # does not print
        print(f'username : {username}')
        if username != 'AnonymousUser':
            # user.username cannot be used directly with get() or filter()
            u_prof = UserProfile.objects.get(user__username=username)
            # does not print
            print(f'retrieved user profile: {u_prof}')
            if save_info:
                u_prof.default_phone_number = shipping_details.phone
                u_prof.default_street_1 = shipping_details.address.line1
                u_prof.default_street_2 = shipping_details.address.line2
                u_prof.default_town_city = shipping_details.address.city
                u_prof.default_county = shipping_details.address.state
                u_prof.default_postcode = shipping_details.address.postal_code
                u_prof.default_country = shipping_details.address.country
                u_prof.save()

        order_exists = False
        # Delay of 1 second each time.
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    street_1__iexact=shipping_details.address.line1,
                    street_2__iexact=shipping_details.address.line2,
                    town_city__iexact=shipping_details.address.city,
                    county__iexact=shipping_details.address.state,
                    postcode__iexact=shipping_details.address.postal_code,
                    country__iexact=shipping_details.address.country,
                    grand_total=grand_total,
                    original_basket=basket,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                # Increment attempt and sleep for 1 second.
                attempt += 1
                time.sleep(1)
        if order_exists:
            self._send_email(order)
            return HttpResponse(
                content=f'WH: {event['type']} | SUCCESS: ORDER EXISTS.',
                status=200,
                content_type='text/plain'
            )
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    useu_prof=u_prof,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_city=shipping_details.address.city,
                    street_1=shipping_details.address.line1,
                    street_2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    original_basket=basket,
                    stripe_pid=pid,
                )
                # Converts from JSON format to Python dictionary.
                # .items() returns an object with key:value tuple pairs.
                for book_id, book_data in json.loads(basket).items():
                    book = Book.objects.get(id=book_id)
                    if isinstance(book_data, int):
                        book_line_item = BookLineItem(
                            order=order,
                            book=book,
                            quantity=book_data,
                        )
                        book_line_item.save()
                    else:
                        book = get_object_or_404(Book, pk=book_id)
                        # Indented in conformance with PEP8 line length.
                        for type, quantity in book_data[
                            'books_by_type'
                        ].items():
                            book_line_item = BookLineItem(
                                order=order,
                                book=book,
                                type=type,
                                quantity=book_data['books_by_type'][type],
                            )
                            book_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                    # Does not show up in Stripe but status matches.
                    return HttpResponse(
                        content=f'WH: {event['type']} | ERROR: {e}.',
                        status=500
                    )
        # Does not show up in Stripe but status is 200.
        self._send_email(order)
        return HttpResponse(
            content=f'WH: {event['type']} | SUCCESS: ORDER CREATED',
            status=200,
            content_type='text/plain'
        )

    def handle_payment_intent_failed(self, event):
        """
        Handles the payment_intent.payment_failed webhook from Stripe.

        Arguments:
        event : JSON object : event data sent by Stripe with all details
        relating to the payment.
        """
        # Does not show up in Stripe but status is 200.
        return HttpResponse(
            content=f'WH: {event['type']}',
            status=200,
            content_type='text/plain'
        )
