from django.urls import path
from .views import *


urlpatterns = [
    path('me/', my_profile, name='user_profile'),
    path('my_books/', my_books, name='user_books'),
    path('review/<int:id>/', leave_review, name='leave_review'),
    path('delete_review/<int:id>/', delete_review, name='delete_review'),
    path('me/update_review/<int:id>/', update_review, name='update_review'),
]
