from django.http import HttpResponse

from .models import *
from library.models import *

import json
import time


class StripeWH_Handler():
    """
    A class for handling Stripe Webhooks.
    """
    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handles generic/unknown/unexpected webhook events.
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event['type']}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handles the payment_intent.succeeded webhook from Stripe.
        """
        intent = event.data.object
        pid = intent.id
        basket = intent.metadata.basket
        save_info = intent.metadata.save_info

        billing_details = stripe_charge.billing_details
        shipping_details = intent.shipping
        grand_total = round(stripe_charge.amount / 100, 2)

        order_exists = False
        # Delay
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_city__iexact=shipping_details.address.city,
                    street_1__iexact=shipping_details.address.line1,
                    street_2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
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
            return HttpResponse(
                content=f'Webhook received: {event['type']} | SUCCESS: Verified order already exists.',
                status=200,
                content_type='text/plain'
            )
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
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
                        content=f'''Webhook received: {event['type']} |
                        ERROR: {e}.''',
                        status=500
                    )
        # Does not show up in Stripe but status is 200.
        return HttpResponse(
            content=f'Webhook received: {event['type']}',
            status=200,
            content_type='text/plain'
        )

    def handle_payment_intent_failed(self, event):
        """
        Handles the payment_intent.payment_failed webhook from Stripe.
        """
        # Does not show up in Stripe but status is 200.
        return HttpResponse(
            content=f'Webhook received: {event['type']} | SUCCESS: Order created in webhook.',
            status=200,
            content_type='text/plain'
        )
