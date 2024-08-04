from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages

from library.models import Book, Genre
from checkout.models import Order, BookLineItem
from .models import UserProfile
from .forms import UserProfileForm


def my_profile(request):
    """
    A view for accessing the user's profile.
    """
    reader = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=reader)
        if form.is_valid:
            form.save()
            messages.success(
                request,
                'Your information has been saved!'
            )

    form = UserProfileForm(instance=reader)
    book_orders = reader.orders.all()
    print(book_orders)

    context={
        'reader': reader,
        'form': form,
        'book_orders': book_orders,
        'profile_page': True
    }
    return render(
        request,
        'reader/profile.html',
        context
    )

def my_books(request):
    """
    A view for rendering the user's books.
    """
    # Retrieve the user's profile (and user).
    user_profile = UserProfile.objects.get(user=request.user)
    # Retrieve their orders.
    user_orders = Order.objects.filter(user_profile=user_profile)

    # Iterate over orders and extend (merge) booklineitems into a list.
    user_booklineitems = []
    for order in user_orders:
        books = order.booklineitem.all()
        # .append() appends quersets to list.
        user_booklineitems.extend(books)

    # Iterate over booklineitems and access book directly (1 instance per book).
    user_books = []
    user_genres = []
    for item in user_booklineitems:
        if item.book not in user_books:
            user_books.append(item.book)
        if item.book.genre not in user_genres:
            user_genres.append(item.book.genre)
    print(user_genres)

    context={
        'user_books': user_books,
        'user_genres': user_genres,
    }
    
    return render(
        request,
        'reader/profile_books.html',
        context
    )