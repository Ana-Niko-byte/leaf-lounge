from django.urls import path
from .views import *


urlpatterns = [
    path('community/', community_general, name='communities'),
    path('community/<slug:slug>', community, name='community'),
]
