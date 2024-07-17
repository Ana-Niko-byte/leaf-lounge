from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.contrib import messages

from library.models import *


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
        messages.add_message(
            request, messages.SUCCESS,
            '''Your book order has been updated! :)'''
        )
    else:
        basket[book_id] = quantity
        messages.add_message(
            request, messages.SUCCESS,
            '''Your book has been added to basket! :)'''
        )

    request.session['basket'] = basket
    return redirect(redirect_url)


def amend_basket(request, book_id):
    '''
    A view for amending items in the basket.
    '''
    quantity = int(request.POST.get('quantity'))
    basket = request.session.get('basket', {})

    if book_id in list(basket.keys()):
        basket[book_id] = quantity
        messages.add_message(
            request, messages.SUCCESS,
            '''Your book order has been updated! :)'''
        )
    else:
        basket[book_id] += quantity
        messages.add_message(
            request, messages.SUCCESS,
            '''Your book order has been updated! :)'''
        )

    request.session['basket'] = basket
    return redirect(reverse('basket'))


def delete_basket(request, book_id):
    '''
    A view for deleting items from the basket.
    '''
    if request.method == 'DELETE':
        basket = request.session['basket']
        if book_id in list(basket.keys()):
            basket.pop(book_id)
            messages.add_message(
                request, messages.SUCCESS,
                '''Your book was successfully deleted.'''
            )
            request.session['basket'] = basket
    return HttpResponseRedirect(reverse('basket'))
