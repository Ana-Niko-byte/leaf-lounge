from django.urls import path
from .views import *

urlpatterns = [
    path('', blurb, name='home'),
    path('contact/', contact, name='contact')
]
