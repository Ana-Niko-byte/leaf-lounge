from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone

from library.models import Book, Genre, Review, Author
from checkout.models import Order, BookLineItem
from .models import UserProfile
from .forms import UserProfileForm, ReviewForm

import logging
logger = logging.getLogger("django")

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

    review_form = ReviewForm()
    form = UserProfileForm(instance=reader)
    book_orders = reader.orders.all()
    user_reviews = Review.objects.filter(reviewer=reader)

    context={
        'reader': reader,
        'form': form,
        'review_form': review_form,
        'book_orders': book_orders,
        'user_reviews': user_reviews,
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

    # Check if the user is a registered author.
    is_author = Author.objects.get(user_profile=user_profile)
    my_books = Book.objects.filter(author=is_author)

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

    if 'genre' in request.GET:
        # .../my_books/?genre=crime
        user_genre = request.GET.getlist('genre')[0]
        if not user_genre:
            messages.error(
                request,
                'An error occurred. Please search for your book in the genre carousels below.'
            )
            return redirect(reverse('user_books'))
        else:
            filtered_books = []
            for book in user_books:
                if str(book.genre) == user_genre:
                    filtered_books.append(book)
            context = {
                'filtered_books': filtered_books,
                'user_genre': user_genre,
                'user_genres': user_genres,
                'chosen': True,
            }
            return render(
                request,
                'reader/profile_books.html',
                context
            )

    context={
        'user_books': user_books,
        'user_genres': user_genres,
        'is_author': is_author,
        'my_books': my_books,
    }
    
    return render(
        request,
        'reader/profile_books.html',
        context
    )


def leave_review(request, id):
    """
    A view for users to leave a book review.
    """
    user_profile = UserProfile.objects.get(user=request.user)
    review_book = get_object_or_404(Book, id=id)

    if request.method == 'POST':
        reviewForm = ReviewForm(request.POST)
        if reviewForm.is_valid():
            review = reviewForm.save(commit=False)
            review.reviewer = user_profile
            review.approved = False
            review.save()
            messages.success(
                request,
                'Thank you for your review! It should be approved within 2 business days :)'
            )
            return redirect('user_books')
        else:
            messages.error(
                request,
                'Please double check your fields and correct errors.'
            )
            reviewForm = ReviewForm()

            context = {
            'reviewForm': reviewForm,
            'review_book': review_book,
            }

            return render(
                request,
                'reader/review.html',
                context
            )
    else:
        reviewForm = ReviewForm()
        context = {
            'reviewForm': reviewForm,
            'review_book': review_book,
        }
        return render(
            request,
            'reader/review.html',
            context
        )


def delete_review(request, id):
    """
    A view for users to delete their reviews.
    """
    try:
        review_delete = get_object_or_404(Review, id=id)
        user_profile = UserProfile.objects.get(user=request.user)
        # Redundant but just in case.
        if review_delete.reviewer == user_profile:
            review_delete.delete()
            messages.success(
                request,
                """Your review for successfully deleted!"""
            )
        else:
            messages.error(
                request,
                """You don't have permission to delete this review.
                If this is a mistake, please contact our customer support team for assistance."""
            )
    except Exception as e:
        print(f'An error occurred while trying to delete a review: {e}')
    finally:
        return HttpResponseRedirect(reverse('user_profile'))


def update_review(request, id):
    """
    A view for users to update their reviews and save them to the database.
    """
    try:
        if request.method == 'POST':
            review_to_update = get_object_or_404(Review, id=id)
            user_profile = UserProfile.objects.get(user=request.user)
            review_form = ReviewForm(request.POST, instance=review_to_update)

            # Redundant but just in case.
            if review_to_update.reviewer == user_profile:
                if review_form.is_valid():
                    review = review_form.save(commit=False)
                    review.reviewer = user_profile
                    review.reviewed_on = timezone.now().date()
                    review.approved = False
                    review.save()
                    messages.success(
                        request,
                        """
                        Your review was successfully updated!
                        Our administrators aim to approve it within 2 business days :)
                        """
                    )
                    return HttpResponseRedirect(reverse('user_profile'))
                else:
                    # Add context to keep the review-slider open for form error rendering.
                    review_form = ReviewForm()
                    messages.error(
                        request,
                        """There is an error in your form.
                        Please fix it or click cancel to finish editing."""
                    )
                    return HttpResponseRedirect(reverse('user_profile'))
                    
            else:
                messages.error(
                    request,
                    """You don't have permission to delete this review.
                    If this is a mistake, please contact our customer support team for assistance."""
                )
                return HttpResponseRedirect(reverse('user_profile'))
        else:
            review_form = ReviewForm
            return HttpResponseRedirect(reverse('user_profile'))

    except Exception as e:
        logger.error(f"An error occurred while trying to update a review: {e}")
        return HttpResponseRedirect(reverse('user_profile'))
