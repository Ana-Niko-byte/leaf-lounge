from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone

from library.models import Book, Genre, Review, Author
from checkout.models import Order, BookLineItem
from .models import UserProfile
from .forms import UserProfileForm, ReviewForm


def my_profile(request):
    """
    This view handles user access and amendments to their user
    profile. If the relevant user profile is not found, the view
    displays a 404 page.

    This view acceps a POST request method and validates the
    UserProfile form for saving user information to their profile.
    This streamlines the checkout process by pre-filling the checkout
    form on the checkout page.

    Returns:
    Redirect: If POST, redirects to the user profile page.
    Render: Renders the user's profile page with the appropriate
    context object.
    """
    reader = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=reader)
        if user_form.is_valid:
            user_form.save()
            messages.success(
                request,
                "Your information has been saved!"
            )
        else:
            messages.error(
                request,
                """
                Please double check your information and try again.
                If the error persists, please get in touch with our
                dedicated customer support team to resolve
                this issue.
                Thank you for your understanding!
                """
            )
        return redirect('user_profile')

    review_form = ReviewForm()
    user_form = UserProfileForm(instance=reader)
    book_orders = reader.orders.all()
    user_reviews = Review.objects.filter(reviewer=reader)

    context = {
        'reader': reader,
        'user_form': user_form,
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
    This view handles the retrieval and display of the user's
    registered (authored) and purchased books. If the relevant profile
    isn't found, the view renders a 404 page.
    """
    # Retrieve the user's profile.
    user_profile = get_object_or_404(UserProfile, user=request.user)

    # Check if the user is a registered author.
    is_author = False
    if Author.objects.filter(user_profile=user_profile):
        is_author = True

    my_books = Book.objects.filter(author=Author.objects.get(user_profile=user_profile))

    # Retrieve their orders.
    user_orders = Order.objects.filter(user_profile=user_profile)

    # Iterate over orders and extend (merge) booklineitems into a list.
    user_booklineitems = []
    for order in user_orders:
        books = order.booklineitem.all()
        # .append() appends quersets to list.
        user_booklineitems.extend(books)

    # Iterate over booklineitems and access book instances directly.
    user_books = []
    user_genres = []
    for item in user_booklineitems:
        if item.book not in user_books:
            user_books.append(item.book)
        if item.book.genre not in user_genres:
            user_genres.append(item.book.genre)

    if 'genre' in request.GET:
        user_genre = request.GET.getlist('genre')[0]
        if not user_genre:
            messages.error(
                request,
                """Something\'s gone wrong - please try again. If the error
                persists, please get in touch with our dedicated customer
                support team to resolve this issue.
                Thank you for your understanding!"""
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

    context = {
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
                """Thank you for your review! It should be approved within 2
                business days :)
                You can view any pending reviews in 'My Profile', under the
                'My Reviews' tab."""
            )
            return redirect('user_books')
        else:
            messages.error(
                request,
                """Please double check your information and correct any errors.
                If the error persists, please get in touch with our dedicated
                customer support team to resolve this issue.
                Thank you for your understanding!
                """
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
            """You don't have permission to delete this review. If this is a
            mistake, please contact our customer support team for
            assistance."""
        )
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
                        Our administrators aim to approve it within 2 business
                        days :)
                        You can view any pending reviews in 'My Profile',
                        under the 'My Reviews' tab.
                        """
                    )
                    return HttpResponseRedirect(reverse('user_profile'))
                else:
                    # Add context to keep review-slider open for form errors.
                    review_form = ReviewForm()
                    messages.error(
                        request,
                        """Please double check your information and correct any
                        errors.
                        If the error persists, please get in touch with our
                        dedicated customer support team to resolve
                        this issue.
                        Thank you for your understanding!
                        """
                    )
                    return HttpResponseRedirect(reverse('user_profile'))
            else:
                messages.error(
                    request,
                    """You don't have permission to delete this review.
                    If this is a mistake, please contact our customer support
                    team for assistance."""
                )
                return HttpResponseRedirect(reverse('user_profile'))
        else:
            review_form = ReviewForm
            return HttpResponseRedirect(reverse('user_profile'))

    except Exception as e:
        return HttpResponseRedirect(reverse('user_profile'))
