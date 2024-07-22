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
            'orderForm': order_form
        }
    )