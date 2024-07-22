from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import *


def checkout(request):
    basket = request.session.get('basket', {})
    if not basket:
        messages.error(
            request,
            'There is nothing in your basket'
        )
        return redirect(reverse('library'))
    
    order_form = OrderForm()

    return render(
        request,
        'checkout/checkout.html',
        {
            'orderForm': order_form,
            'stripe_public_key': 'pk_test_51PfSh4J7pjNjyBYl3N4sE0VmMv8NXlFPwPz3ZLbiqaqyhUQbwG7F7F95tqVKHBHHfyxmXtS93nEvm7BwHQSfJvLl00qfWIwuGO',
            'client_secret': 'test client secret key',
        }
    )