from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

# Create your views here.
def my_profile(request, user_id):
    """
    A view for accessing the user's profile.
    """
    reader = get_object_or_404(User, id=user_id)
    context={
        'reader': reader,
    }
    return render(
        request,
        'reader/profile.html',
        context
    )