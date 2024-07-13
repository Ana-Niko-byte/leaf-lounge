from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from .models import *


def library(request):
    books = Book.objects.all()
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

            queries = Q(title__icontains=query)
            books = books.filter(queries)

    context = {
        'books': books,
        'search_term' : query,
    }
    return render(
        request,
        'library/library.html',
        context
    )


def book_detail(request, slug):
    requested_book = get_object_or_404(Book,slug=slug)
    print(requested_book)

    context={
        'book': requested_book,
    }

    return render(
        request,
        "library/book_detail.html",
        context
    )