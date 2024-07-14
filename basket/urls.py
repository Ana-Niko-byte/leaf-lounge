from django.urls import path
from .views import *

urlpatterns = [
    path('', basket, name='basket'),
    path('add/<int:book_id>', add_basket, name='add_to_basket'),
]
