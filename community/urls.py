from django.urls import path
from .views import *


urlpatterns = [
    path('community/', community_general, name='communities'),
    path('community/<slug:slug>', community, name='community'),
    path('become/author/', create_author, name='create_author'),
    path('become/author/book', upload_book, name='upload_book'),
]
