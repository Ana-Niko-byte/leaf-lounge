from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.shortcuts import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

from basket.contexts import bag_content
from reader.models import UserProfile
from library.models import Book
from reader.forms import UserProfileForm
from .forms import *
from .models import *

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
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'basket': json.dumps(request.session.get('basket', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
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
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_basket = json.dumps(basket)
            order.save()
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

        if request.user.is_authenticated:
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': user_profile.user.get_full_name(),
                    'email': user_profile.user.email,
                    'phone_number': user_profile.default_phone_number,
                    'country': user_profile.default_country,
                    'postcode': user_profile.default_postcode,
                    'town_city': user_profile.default_town_city,
                    'street_1': user_profile.default_street_1,
                    'street_2': user_profile.default_street_2,
                    'county': user_profile.default_county,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
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
    A view for handling successful checkouts and displaying the order confirmation.
    """
    save_info = request.session.get('save_info')
    book_order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        book_order.user_profile = user_profile
        book_order.save()

    if save_info:
        reader_data = {
            'default_phone_number': book_order.phone_number,
            'default_country': book_order.country,
            'default_postcode': book_order.postcode,
            'default_town_city': book_order.town_city,
            'default_street_1': book_order.street_1,
            'default_street_2': book_order.street_2,
            'default_county': book_order.county,
        }

        user_profile_form = UserProfileForm(reader_data, instance=user_profile)
        if user_profile_form.is_valid():
            user_profile_form.save()

    # if request.user.is_authenticated:
    #     email = user_profile.user.email
    #     send_mail(
    #         subject=f"Your Order Confirmation {order_number}",
    #         message=f"Thank you for your order! Your order number is {order_number}",
    #         from_email=settings.EMAIL_HOST_USER,
    #         recipient_list=[f"{email}"],
    #         fail_silently=False,
    #     )
    # else:
    #     email = book_order.email
    #     send_mail(
    #         subject=f"Your Order Confirmation {order_number}",
    #         message=f"Thank you for your order! Your order number is {order_number}",
    #         from_email=settings.EMAIL_HOST_USER,
    #         recipient_list=[f"{email}"],
    #         fail_silently=False,
    #     )

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
