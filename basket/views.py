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
    # book = Book.objects.get(pk=book_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    type = None
    if 'book_type' in request.POST:
        type = request.POST['book_type']
    basket = request.session.get('basket', {})

    if type:
        # Without map, comparison was between an int and str values, hence always false.
        if book_id in list(map(int, basket.keys())):
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
        else:
            basket[book_id] = quantity

    request.session['basket'] = basket
    return redirect(redirect_url)


def amend_basket(request, book_id):
    '''
    A view for amending items in the basket.
    '''
    quantity = int(request.POST.get('quantity'))
    type = None
    if 'book_type' in request.POST:
        type = request.POST['book_type']
    basket = request.session.get('basket', {})

    if type:
        if quantity > 0:
            basket[book_id]['books_by_type'][type] = quantity
        else:
            # Form will not submit if quantity is less than 0 or greater than 99 but as a fall back...
            del basket[book_id]['books_by_type'][type]
            if not basket[book_id]['books_by_type']:
                basket.pop(book_id)
    else:
        if quantity > 0:
            basket[book_id] = quantity
        else:
            basket.pop(book_id)

    request.session['basket'] = basket
    return redirect(reverse('basket'))
    

def delete_basket(request, book_id):
    '''
    A view for deleting items from the basket.
    '''
    try:
        type = None
        if 'book_type' in request.POST:
            type = request.POST['book_type']
        basket = request.session.get('basket', {})

        if type:
            del basket[book_id]['books_by_type'][type]
            if not basket[book_id]['books_by_type']:
                basket.pop(book_id)
        else:
            basket.pop(book_id)

        request.session['bag'] = basket
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=500)