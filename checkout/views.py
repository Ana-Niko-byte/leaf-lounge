from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings

from .forms import *
from .models import *
from library.models import Book
from basket.contexts import bag_content

import stripe


def checkout(request):
    """

    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        basket = request.session.get('basket', {})
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
                        for type, quantity in book_data['books_by_type'].items():
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
        basket = request.session.get('basket', {})
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
        }
    )


def success(request, order_number):
    """

    """
    save_info = request.session.get('save_info')
    book_order = get_object_or_404(Order, order_number=order_number)
    messages.success(
        request,
        f"""Your order has been placed!/ 
        Order Number: {order_number}. A confirmation email will
        be sent to the email address indicated on your order."""
    )
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
