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
    Handles the caching of checkout data in the Stripe PaymentIntent metadata.

    This view is responsible for updating the metadata of a Stripe
    PaymentIntent with information from the user's session and POST data.
    It extracts the PaymentIntent ID from the client secret and updates the
    PaymentIntent with details about the user's basket. Additionally, it checks
    whether the user has opted to save their billing information to their
    profile under the 'My Profile' tab for faster future checkouts.

    The view requires a POST request and will return a 200 HTTP status code if
    the metadata update is successful. If an error occurs during the process,
    the view will display an error message to the user and return a 400 HTTP
    status code.

    POST Data:
    client_secret (str): The client secret from the Stripe PaymentIntent.
    save_info (str, optional): A boolean checkbox indicating the user's intent
    to save their billing information to their profile.

    Returns:
    HttpResponse: An HTTP response with a status code of 200 if the update is
    successful, or 400 with an error message if an exception occurs.

    Decorators:
    @require_POST: Ensures that the view only accepts POST requests.
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
            """
            Sorry, your payment cannot be processed at this time.
            Please try again - If the error persists, please get
            in touch with our dedicated customer support team to
            resolve this issue.
            Thank you for your understanding!
            """
        )
        return HttpResponse(content=e, status=400)


def checkout(request):
    """
    Handles the checkout process for users, including collecting order details,
    processing payment, and saving order information.

    This view manages the checkout workflow for users who wish to place a book
    order. It displays a checkout form and processes form submissions.

    A GET request will initialise a Stripe payment intent, and display the
    checkout form with pre-filled user information if the user is authenticated
    and has opted to save their billing information to their profile in a
    previous order.

    A POST request will validate the submitted form data, process the order and
    redirect the user to a success page upon successful payment.

    If any item in the user's basket is no longer available, an error message
    is displayed, and the user is redirected back to their basket.

    POST Data:
    OrderForm values: e.g., full_name, email, phone_number, etc.
    client_secret (str): The client secret from the Stripe PaymentIntent.

    Returns:
    HttpResponse: Renders the checkout page with the order form and Stripe
    payment intent.
    HttpResponseRedirect: Redirects to the basket page if the basket is empty
    or a book is no longer available.
    HttpResponseRedirect: Redirects to the order success page after successful
    payment.
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
                """Please correct issues in the form below and re-submit.
                If the error persists, please get in touch with our
                dedicated customer support team to resolve
                this issue.
                Thank you for your understanding!"""
            )
    else:
        if not basket:
            messages.error(
                request,
                "There is nothing in your basket"
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

        # Pre-fill fields with user's existing information.
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
        messages.error(
            request,
            """
            It seems our payments system is temporarily down.
            Please contact our dedicated customer support team
            directly to place your order and we'll throw in an extra
            10% off for the inconvenience.
            Thank you for your understanding!
            """
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
    This view handles the display of an order summary table and key order
    information after a successful checkout process.
    """
    save_info = request.session.get('save_info')
    book_order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        book_order.user_profile = user_profile
        book_order.save()

    if save_info:
        reader_data = {
            'default_full_name': book_order.full_name,
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

    context = {
        'book_order': book_order,
        'order_number': order_number,
    }

    if 'basket' in request.session:
        del request.session['basket']

    return render(
        request,
        'checkout/success.html',
        context
    )
