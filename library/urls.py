from django.urls import path
from .views import *

urlpatterns = [
    path('', library, name='library'),
    path('book/<slug:slug>/', book_detail, name='book-summary'),
    path('review/', leave_review, name='leave_review'),
]
