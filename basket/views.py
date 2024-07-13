from django.shortcuts import render
from django.contrib import messages


def basket(request):

    return render(
        request,
        'basket/basket.html'
    )