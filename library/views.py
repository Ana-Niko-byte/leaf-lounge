from django.shortcuts import render

from.models import *


def library(request):
    books = Book.objects.all()
    context = {
        'books': books,
    }
    return render(
        request,
        'library/library.html',
        context
    )
