from django.urls import path
from .views import *

urlpatterns = [
    path('', library, name='library'),
]
