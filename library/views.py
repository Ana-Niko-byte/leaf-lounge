from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from .models import *


def library(request):
    """
    A view for displaying Book model instances in the library.
    """
    books = Book.objects.all()
    authors = Author.objects.all()
    genres = Genre.objects.all()
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

        elif 'author' in request.GET:
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

        elif 'genre' in request.GET:
            book_genres = request.GET.getlist('genre')
            if not book_genres:
                messages.error(
                    request,
                    'Please select the genres you wish to filter by.'
                )
                return redirect(reverse('library'))
            else:
                for genre in book_genres:
                    filter_query |= Q(genre__icontains=genre)
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
        'genres': genres,
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
