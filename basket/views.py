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
    type = None
    if 'book_type' in request.POST:
        type = request.POST['book_type']
    basket = request.session.get('basket', {})

    if type:
        # Without map, comparison was between an int and str values, hence always false
        print(list(map(int, basket.keys())))
        if book_id in list((map(int, basket.keys()))):

            if type in basket[f'{book_id}']['books_by_type'].keys():
                basket[f'{book_id}']['books_by_type'][type] += quantity
            else:
                basket[f'{book_id}']['books_by_type'][type] = quantity
        else:
            basket[book_id] = {'books_by_type' : {type : quantity}}

    # Is this needed? all books have type? Perhaps best to leave as fall back.
    else:
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
        # if quantity == 0:
        #    messages.add_message(
        #     request, messages.error,
        #     '''Please ensure quantity is greater than 0 or delete the item'''
        # ) 
        # else:
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
