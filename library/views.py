from django.shortcuts import render, redirect, reverse
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
