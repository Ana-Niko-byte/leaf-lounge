from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count

from .models import *
from reader.models import UserProfile
from .forms import ReviewForm

from itertools import product


def library(request):
    """
    A view for displaying Book model instances in the library.
    """
    books = Book.objects.all()
    authors = Author.objects.all().order_by('first_name')
    # __gt >> greater than.
    # .distinct() >> unique values.
    filtered_genres = Genre.objects.filter(book_genre__gt=0).order_by('name').distinct()
    # Add book counts to filtered_genres - ANNOTATE()

    query = None
    filter_query = Q()

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request,
                    'Please enter the title of the book you are searching for.'
                )
                return redirect(reverse('library'))
            queries = Q(title__icontains=query)
            books = books.filter(queries)

        elif 'author' and 'genre' in request.GET:
            authors_ln = request.GET.getlist('author')
            book_genres = request.GET.getlist('genre')
            if not authors_ln and not book_genres:
                messages.error(
                    request,
                    'You didn\'t select any filters.'
                )
                return redirect(reverse('library'))
            else:
                merged_query = Q()
                for author, genre in product(authors_ln, book_genres):
                    merged_conditions = Q(
                        author__last_name__icontains=author
                    ) and Q(
                        genre__name__icontains=genre
                    )
                    merged_query |= merged_conditions
                books = books.filter(merged_query)

            if 'author' in request.GET and 'genre' not in request.GET:
                authors_ln = request.GET.getlist('author')
                if not authors_ln:
                    messages.error(
                        request,
                        'Please select the authors you wish to filter by.'
                    )
                    return redirect(reverse('library'))
                else:
                    for item in authors_ln:
                        # |= OR Query, searching author__last_name
                        # enabled in admin.py.
                        filter_query |= Q(author__last_name__icontains=item)
                    books = books.filter(filter_query)
                    # As authors_ln is not passed to context unless
                    # user always includes an author filter.
                    context = {
                        'books': books,
                        'genres': genres,
                        'authors': authors,
                        'search_term': query,
                        'authors_ln': authors_ln,
                    }
                    return render(
                        request,
                        'library/library.html',
                        context
                    )

            elif 'genre' in request.GET and 'author' not in request.GET:
                book_genres = request.GET.getlist('genre')
                if not book_genres:
                    messages.error(
                        request,
                        'Please select the genres you wish to filter by.'
                    )
                    return redirect(reverse('library'))
                else:
                    for genre in book_genres:
                        filter_query |= Q(genre__name__icontains=genre)
                    books = books.filter(filter_query)
                    context = {
                        'books': books,
                        'genres': genres,
                        'authors': authors,
                        'search_term': query,
                        'book_genres': book_genres,
                    }
                    return render(
                        request,
                        'library/library.html',
                        context
                    )

    context = {
        'books': books,
        'filtered_genres': filtered_genres,
        'authors': authors,
        'search_term': query,
    }
    return render(
        request,
        'library/library.html',
        context
    )


def book_detail(request, slug):
    """
    A view for displaying more information on each book.
    """
    requested_book = get_object_or_404(Book, slug=slug)
    types = Book.COVERS

    context = {
        'book': requested_book,
        'types': types,
    }

    return render(
        request,
        'library/book_detail.html',
        context
    )


def leave_review(request):
    """
    """
    user_profile = UserProfile.objects.get(user=request.user)

    reviewForm = ReviewForm()
    if request.method == 'POST':
        if reviewForm.is_valid():
            reviewForm.save()
        else:
            messages.error(
                request,
                'Please double check your fields and correct errors.'
            )
            reviewForm = ReviewForm()

    context = {
        'reviewForm': reviewForm,
    }

    return render(
        request,
        'library/review.html',
        context
    )
