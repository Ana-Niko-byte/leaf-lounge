from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from .models import *
from ._genres import GENRES


def library(request):
    """
    A view for displaying Book model instances in the library.
    """
    books = Book.objects.all()
    authors = Author.objects.all()
    books_adventure = books.filter(genre='Adventure')
    genres = [genre[1] for genre in GENRES]
    print(authors)
    query = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request,
                    'Please enter the title of the book you are searching for.'
                )
                return redirect(reverse('library'))

            # incorporate search by author later
            queries = Q(title__icontains=query)
            books = books.filter(queries)

    context = {
        'books': books,
        'genres': genres,
        'authors': authors,
        'search_term' : query,
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
        'types' : types,
    }

    return render(
        request,
        'library/book_detail.html',
        context
    )
