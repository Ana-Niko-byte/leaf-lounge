from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from library.models import *


def basket(request):
    """
    Retrieves and displays the details and contents of a user's basket.
    """
    return render(
        request,
        'basket/basket.html'
    )


def add_basket(request, book_id):
    """
    Handles the addition of books to a user's shopping basket based on the
    provided book ID and specified quantity.

    This view is responsible for adding a book to the user's session basket.
    Before adding the book, the view checks whether the book is already in the
    basket. If it is, the book quantity is updated, else, a new entry is added.

    The user can specify different cover types for the book - as specified in
    the model, and the view will manage the quantities accordingly. If the book
    type is provided, it ensures that the correct type and quantity are
    recorded in the session.

    If the specified book is not found in the database, a 404 error will be
    raised. After successfully adding or updating a book entry, a success
    message is displayed to the user, and the user is redirected to the
    appropriate view.

    Additional Parameters:
    book_id (int): The ID of the book to be added to the basket.

    POST Data:
    quantity (int): The quantity of books to add to the basket.
    redirect_url (url) : The URL to redirect the user to after processing.
    book_type (str, optional): The book cover type.

    Returns:
    HttpResponseRedirect: Redirects the user to the specified URL.
    Raises:
    Http404: If the book with the specified ID does not exist in the database.
    """
    book = get_object_or_404(Book, pk=book_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    type = None
    if 'book_type' in request.POST:
        type = request.POST['book_type']
    basket = request.session.get('basket', {})

    if type:
        # Without map, comparison was between an int and str values, hence
        # always false.
        if book_id in list(map(int, basket.keys())):
            if type in basket[f'{book_id}']['books_by_type'].keys():
                basket[f'{book_id}']['books_by_type'][type] += quantity
                messages.success(
                    request,
                    f"'{book.title}' has been updated in your basket."
                )
            else:
                basket[f'{book_id}']['books_by_type'][type] = quantity
                messages.success(
                    request,
                    f"'{book.title}' has been added to your basket."
                )
        else:
            basket[book_id] = {'books_by_type': {type: quantity}}
            messages.success(
                request,
                f"'{book.title}' has been added to your basket."
            )

    request.session['basket'] = basket
    return redirect(redirect_url)


def amend_basket(request, book_id):
    """
    This view handles user amendments made to the book quantities in a
    session basket.

    Additional Parameters:
    book_id (int): The ID of the book to be added to the basket.

    POST Data:
    quantity (int): The quantity of books to add to the basket.
    type (str, optional): The book cover type.

    Returns:
    HttpResponseRedirect: Redirects the user back to the basket view.
    """
    quantity = int(request.POST.get('quantity'))
    type = None
    if 'book_type' in request.POST:
        type = request.POST['book_type']
    basket = request.session.get('basket', {})

    if type:
        if quantity > 0:
            basket[book_id]['books_by_type'][type] = quantity
            messages.success(
                request,
                f"Quantity has been successfully updated!"
            )
        else:
            # Form will not submit if quantity is less than 0 or greater
            # than 99 but as a fall back...
            del basket[book_id]['books_by_type'][type]
            if not basket[book_id]['books_by_type']:
                basket.pop(book_id)

    request.session['basket'] = basket
    return redirect(reverse('basket'))


def delete_basket(request, book_id):
    """
    This view handles the deletion of book instances from the session basket.

    Additional Parameters:
    book_id (int): The ID of the book to be added to the basket.

    POST Data:
    type (str, optional): The book cover type.

    Returns:
    HttpResponse: 200 for successful deletions.
    HttpResponse: 500 for unsuccessful deletions.
    """
    try:
        type = None
        if 'book_type' in request.POST:
            type = request.POST['book_type']
        basket = request.session.get('basket', {})

        if type:
            del basket[book_id]['books_by_type'][type]
            if not basket[book_id]['books_by_type']:
                basket.pop(book_id)
        messages.success(
            request,
            f"Book has been successfully removed."
        )

        request.session['bag'] = basket
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(
            request,
            f"""An error occurred while attempting to remove
            the book from your basket. Please try again -
            if the error persists, please get in touch with our
            dedicated customer support team to resolve this issue.
            Thank you for your understanding!"""
        )
        return HttpResponse(status=500)
