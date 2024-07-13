from django.shortcuts import get_object_or_404
from django.conf import settings

from decimal import Decimal

from library.models import Book


def bag_content(request):

    FDT = settings.FREE_DELIVERY_THRESHOLD
    basket = request.session.get('basket', {})

    books_in_basket = []
    total = 0
    book_count = 0

    for book_id, quantity in basket.items():
       book = get_object_or_404(Book, pk=book_id)
       total += quantity * book.price
       book_count += quantity 
       books_in_basket.append({
        'book_id': book_id,
        'quantity': quantity,
        'book': book,
       })

    if total > FDT:
        delivery = 0
        free_delivery_delta = 0
    else:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE/100)
        free_delivery_delta = FDT - total

    books_total = delivery + total
    

    context = {
        'books_in_basket': books_in_basket,
        'total': total,
        'book_count': book_count,
        'books_total': books_total,
        'delivery': delivery,
        'FDT' : FDT,
        'free_delivery_threshold': free_delivery_delta  
    }

    return context