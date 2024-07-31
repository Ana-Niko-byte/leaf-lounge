from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from .models import UserProfile

# Create your views here.
def my_profile(request):
    """
    A view for accessing the user's profile.
    """
    # reader = get_object_or_404(UserProfile, user=request.user)
    # print(reader)
    print(request.user)
    # context={
    #     'reader': reader,
    # }
    return render(
        request,
        'reader/profile.html',
        # context
    )