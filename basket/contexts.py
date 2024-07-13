from decimal import Decimal
from django.conf import settings


def bag_content(request):

    FDT = settings.FREE_DELIVERY_THRESHOLD
    books_in_basket = []
    total = 0
    book_count = 0

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