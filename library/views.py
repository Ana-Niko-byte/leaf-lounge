from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count

from .models import *
from reader.models import UserProfile

from itertools import product


def library(request):
    """
    This view is responsible for retrieving and displaying all books in the
    dedicated library page, along with filtering 'by author' and 'by genre',
    and search functionality. This view handles the display of books in genre
    carousels, and displays only those genres which have at least one book
    associated with them. Each book is a link to a dedicated book detail page.

    Users do not need to be registered to view the library.

    Returns:
    Renders: Renders the library page with the relevant context.
    """
    books = Book.objects.all()
    # __gt >> greater than.
    # .distinct() >> unique values.
    filtered_genres = Genre.objects.filter(
        book_genre__gt=0
    ).annotate(
        genre_count=Count(
            'book_genre'
        )).order_by('name').distinct()
    book_count_authors = Author.objects.filter(
        author_books__gt=0
    ).annotate(
        book_count=Count(
            'author_books'
        )).order_by('first_name')

    query = None
    filter_query = Q()

    if request.GET:
        if 'q' in request.GET:
            print('q')
            query = request.GET['q']
            if not query:
                messages.error(
                    request,
                    "Please enter the title of the book you are searching for."
                )
                return redirect(reverse('library'))
            queries = Q(title__icontains=query)
            books = books.filter(queries)
            print(queries)

        if 'author' in request.GET:
            if 'genre' in request.GET:
                authors_ln = request.GET.getlist('author')
                book_genres = request.GET.getlist('genre')
                if not authors_ln and not book_genres:
                    messages.error(
                        request,
                        "You haven\'t select any filters."
                    )
                    return redirect(reverse('library'))
                else:
                    merged_query = Q()
                    for author, genre in product(authors_ln, book_genres):
                        merged_conditions = Q(
                            author__last_name__icontains=author
                        ) & Q(
                            genre__name__icontains=genre
                        )
                        merged_query |= merged_conditions
                    books = books.filter(merged_query)
                    query_books_genres = [book.genre for book in books]
                    if not books:
                        return render(
                            request,
                            'library/no_books.html'
                        )
                    context = {
                        'both': True,
                        'query_book_genres': query_books_genres,
                        'books': books,
                        'books': books,
                        'filtered_genres': filtered_genres,
                        'book_count_authors': book_count_authors,
                        'search_term': query,
                        'authors_ln': authors_ln,
                        'book_genres': book_genres,
                    }
                    return render(
                        request,
                        'library/library.html',
                        context
                    )
            else:
                authors_ln = request.GET.getlist('author')
                if not authors_ln:
                    messages.error(
                        request,
                        "Please select the authors you wish to filter by."
                    )
                    return redirect(reverse('library'))
                else:
                    for item in authors_ln:
                        # |= OR Query, searching author__last_name
                        # enabled in admin.py.
                        filter_query |= Q(author__last_name__icontains=item)
                    books = books.filter(filter_query)
                    context = {
                        'author_search': True,
                        'books': books,
                        'book_count_authors': book_count_authors,
                        'search_term': query,
                        'authors_ln': authors_ln,
                        'filtered_genres': filtered_genres,
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
                    "Please select the genres you wish to filter by."
                )
                return redirect(reverse('library'))
            else:
                for genre in book_genres:
                    filter_query |= Q(genre__name__icontains=genre)
                books = books.filter(filter_query)
                genres_called = []
                [genres_called.append(
                    book.genre
                ) for book in books if book.genre not in genres_called]
                context = {
                    'genre_search': True,
                    'genres_called': genres_called,
                    'books': books,
                    'filtered_genres': filtered_genres,
                    'book_count_authors': book_count_authors,
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
        'book_count_authors': book_count_authors,
        'search_term': query,
        'library_view': True,
    }
    return render(
        request,
        'library/library.html',
        context
    )


def book_detail(request, slug):
    """
    This view handles the display of individual book details
    in a dedicated detail page. If the requested book is not
    found, the view displays a 404 page.
    """
    requested_book = get_object_or_404(Book, slug=slug)
    types = Book.COVERS

    # Rating
    book_reviews = Review.objects.filter(book=requested_book, approved=True)
    ratings = [book.rating for book in book_reviews]

    author_books = Book.objects.filter(
        author=requested_book.author
    ).exclude(title=requested_book.title)

    context = {
        'book': requested_book,
        'ratings': ratings,
        'types': types,
        'detail': True,
        'author_books': author_books,
        'book_reviews': book_reviews,
    }

    return render(
        request,
        'library/book_detail.html',
        context
    )
