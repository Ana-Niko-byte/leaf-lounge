from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from django.contrib import messages

from .forms import EmailForm


def mailchimp_marketing(request):
    """
    Site-wide form context variables for allowing users to subscribe to
    the Leaf Lounge newsletter from every page via the footer.

    Context:
    'marketing_form': (form object) : The Newsletter form that takes the user's email.

    Returns: context object.
    """
    marketing_form = EmailForm()
    context = {
        "marketing_form": marketing_form,
    }

    return context

