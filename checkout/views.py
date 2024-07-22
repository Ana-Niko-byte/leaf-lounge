from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import *
from basket.contexts import bag_content

import stripe


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

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
        messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your env.py?')

    return render(
        request,
        'checkout/checkout.html',
        {
            'orderForm': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
        }
    )