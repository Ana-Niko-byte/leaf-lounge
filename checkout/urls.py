from django.urls import path
from .views import *
from .webhooks import webhook

urlpatterns = [
    path('', checkout, name='checkout'),
    path('<order_number>/success', success, name='success'),
    path(
        'cache_checkout_data/', cache_checkout_data, name='cache_checkout-data'
    ),
    path('wh/', webhook, name='webhook'),
]
