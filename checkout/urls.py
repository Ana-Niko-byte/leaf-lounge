from django.urls import path
from .views import *

urlpatterns = [
    path('', checkout, name='checkout'),
    path('<order_number>/success', success, name='success')
]
