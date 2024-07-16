from django.urls import path
from .views import *

urlpatterns = [
    path('', basket, name='basket'),
    path('add/<int:book_id>', add_basket, name='add_to_basket'),
    path('update/<book_id>', amend_basket, name='update_basket'),
    path('delete/<book_id>', delete_basket, name='delete_basket'),
]
