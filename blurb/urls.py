from django.urls import path
from .views import *

urlpatterns = [
    path('', blurb, name='home'),
]