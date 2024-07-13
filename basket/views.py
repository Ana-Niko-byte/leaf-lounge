from django.shortcuts import render, redirect
from django.contrib import messages


def basket(request):
    '''
    The main basket view.
    '''
    return render(
        request,
        'basket/basket.html'
    )


def add_basket(request, book_id):
    '''
    A view for adding items to the basket.
    '''
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    basket = request.session.get('basket', {})

    if book_id in list(basket.keys()):
        basket[book_id] += quantity
    else:
        basket[book_id] = quantity

    request.session['basket'] = basket
    return redirect(redirect_url)
