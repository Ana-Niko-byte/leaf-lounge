from django.urls import path
from .views import *


urlpatterns = [
    path('me/', my_profile, name='user_profile'),
    path('order/<order_number>', order_detail, name='order_detail')
]
