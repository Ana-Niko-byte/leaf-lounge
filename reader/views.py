from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages

from .models import UserProfile
from .forms import UserProfileForm


def my_profile(request):
    """
    A view for accessing the user's profile.
    """
    reader = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=reader)
        if form.is_valid:
            form.save()
            messages.success(
                request,
                'Your information has been saved!'
            )

    form = UserProfileForm(instance=reader)
    book_orders = reader.orders.all()

    context={
        'reader': reader,
        'form': form,
        'book_orders': book_orders,
        'profile_page': True
    }
    return render(
        request,
        'reader/profile.html',
        context
    )