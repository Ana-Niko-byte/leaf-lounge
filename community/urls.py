from django.urls import path
from .views import *


urlpatterns = [
    path('community/', community_general, name='communities'),
    path('community/<slug:slug>', community, name='community'),
    path('forum/<slug:slug>', forum_detail, name='forum_detail'),
    path('become/author/', create_author, name='create_author'),
    path('become/author/book', upload_book, name='upload_book'),
    path('delete/<slug:slug>/<int:id>', delete_message, name='delete_message'),
]
