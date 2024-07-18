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

    # book_data = type & quantity
    for book_id, book_data in basket.items():
        if isinstance(book_data, int):
            book = get_object_or_404(Book, pk=book_id)
            total += book_data * book.price
            indiv_total = book_data * book.price
            book_count += book_data 
            books_in_basket.append({
                'book_id': book_id,
                'quantity': book_data,
                'indiv_total': indiv_total,
                'book': book,
            })
        else:
            book = get_object_or_404(Book, pk=book_id)
            for type, quantity in book_data['books_by_type'].items():
                total += quantity * book.price
                indiv_total = quantity * book.price
                book_count += quantity
                books_in_basket.append({
                    'book_id': book_id,
                    'quantity': quantity,
                    'indiv_total': indiv_total,
                    'book': book,
                    'type': type,
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