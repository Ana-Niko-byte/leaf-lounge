from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.shortcuts import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import *
from .models import *
from library.models import Book
from basket.contexts import bag_content

import stripe
import json


@require_POST
def cache_checkout_data(request):
    """
    A view for updating Stripe PaymentIntent Metadata to handle
    'save_info'.
    """
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        print(pid)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        print(stripe.api_key)
        stripe.PaymentIntent.modify(pid, metadata={
            'basket': json.dumps(request.session.get('basket', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        print('success')
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(
            request,
            '''
            Sorry, your payment cannot be processed at this time.
            Please try again later or contact our customer support team.
            '''
        )
        return HttpResponse(content=e, status=400)


def checkout(request):
    """
    A view for users to checkout and proceed with payment.
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    basket = request.session.get('basket', {})
    order_list = []
    for book_id, book_data in basket.items():
        for type, quantity in book_data['books_by_type'].items():
            order_list.append(quantity)
    basket_items_count = sum(order_list)

    if request.method == 'POST':
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_city': request.POST['town_city'],
            'street_1': request.POST['street_1'],
            'street_2': request.POST['street_2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(data=form_data)
        if order_form.is_valid():
            order = order_form.save()
            order_list = []
            for book_id, book_data in basket.items():
                try:
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
                except Book.DoesNotExist:
                    messages.error(
                        request,
                        """It seems one of the books in your basket
                        has been removed from our database. Please
                        contact us via our Contact page to arrange a delivery.
                        Apologies for the inconvenience."""
                    )
                    order.delete()
                    return redirect(reverse('basket'))
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('success', args=[order.order_number]))
        else:
            messages.error(
                request,
                'Please correct issues in the form below and re-submit.'
            )
    else:
        if not basket:
            messages.error(
                request,
                'There is nothing in your basket'
            )
            return redirect(reverse('library'))

        current_basket = bag_content(request)
        basket_total = current_basket['books_total']
        stripe_total = round(basket_total * 100)

        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(
            request,
            '''Stripe public key is missing.
            Did you forget to set it in your env.py?'''
        )

    return render(
        request,
        'checkout/checkout.html',
        {
            'orderForm': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
            'basket_items_count': basket_items_count,
        }
    )


def success(request, order_number):
    """

    """
    save_info = request.session.get('save_info')
    book_order = get_object_or_404(Order, order_number=order_number)
    basket_books = []
    basket = request.session.get('basket', {})
    for book_id, book_data in basket.items():
        book = get_object_or_404(Book, pk=book_id)
        for type, quantity in book_data['books_by_type'].items():
            basket_books.append({
                'book_id': book_id,
                'book_order': book_order,
                'quantity': quantity,
                'book': book,
                'type': type,
            })

    context = {
        'book_order': book_order,
        'order_number': order_number,
        'basket_books': basket_books,
    }

    if 'basket' in request.session:
        del request.session['basket']

    return render(
        request,
        'checkout/success.html',
        context
    )
