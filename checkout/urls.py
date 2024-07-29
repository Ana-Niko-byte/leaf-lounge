from django.urls import path
from .views import *
from .webhooks import webhook

urlpatterns = [
    path('', checkout, name='checkout'),
    path('<order_number>/success', success, name='success'),
    path('wh/', webhook, name='webhook')
]
