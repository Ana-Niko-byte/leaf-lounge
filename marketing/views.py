from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages

from marketing.forms import EmailForm

from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

import hashlib


def subscribe_view(request):
    """
    Handles user subscriptions by processing the subscription form and adding
    the user's email to the Mailchimp mailing list.

    This view accepts POST requests with user email information. On form
    validation, it makes an API call to the Mailchimp service to add the user
    to the mailing list. If the API call is successful, the view redirects the
    user to a success page. If unsuccessful, the user is redirected to the
    fail page.

    Returns:
    HttpResponseRedirect: Redirects to either the success or failure page based
    on the outcome of the Mailchimp API call.

    POST Data:
    email: The email address submitted through the form to be added to the
    Mailchimp list.
    """
    if request.method == 'POST':
        marketing_form = EmailForm(request.POST)
        # marketing_form.fields['email'].widget.attrs.update({'id': 'subscribe-input'})
        if marketing_form.is_valid():
            try:
                form_email = marketing_form.cleaned_data['email']
                member_info = {
                    'email_address': form_email,
                    'status': 'subscribed',
                }
                response = mailchimp.lists.add_list_member(
                    settings.MAILCHIMP_MARKETING_AUDIENCE_ID,
                    member_info,
                )
                messages.success(
                    request, 
                    """
                    You've successfully subscribed to our mailing list! :)
                    """
                )
                return redirect(request.META.get('HTTP_REFERER', '/'))
            except ApiClientError as error:
                messages.error(
                    request,
                    """Our mailing list is currently being updated. 
                    Please try again a bit later or get in touch
                    with our dedicated customer support team to resolve
                    this issue.
                    Thank you for your understanding!"""
                )
                return redirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, 'marketing/subscribe.html', {
        'marketing_form': EmailForm(),
    })


def unsubscribe_view(request):
    """
    Handles user Unsubscriptions by processing the subscription form with the
    user's email.

    This view accepts POST requests with user email information. On form
    validation, it makes an API call to the Mailchimp service to remove the
    user from the mailing list. If the API call is successful, the view
    redirects the user to a success page. If unsuccessful, the user is
    redirected to the fail page.

    Returns:
    HttpResponseRedirect: Redirects to either the success or failure page based
    on the outcome of the Mailchimp API call.

    POST Data:
    email: The email address submitted through the form to be removed from the
    Mailchimp list.
    """
    if request.method == 'POST':
        marketing_form = EmailForm(request.POST)
        # marketing_form.fields['email'].widget.attrs.update({'id': 'unsubscribe-input'})
        if marketing_form.is_valid():
            try:
                form_email = marketing_form.cleaned_data['email']
                form_email_hash = hashlib.md5(
                    form_email.encode('utf-8').lower()
                ).hexdigest()
                member_update = {
                    'status': 'unsubscribed',
                }
                response = mailchimp.lists.update_list_member(
                    settings.MAILCHIMP_MARKETING_AUDIENCE_ID,
                    form_email_hash,
                    member_update,
                )
                messages.success(
                    request, 
                    """
                    You've successfully unsubscribed from our mailing list! :(
                    """
                )
                return redirect(request.META.get('HTTP_REFERER', '/'))
            except ApiClientError as error:
                messages.error(
                    request,
                    """Our mailing list is currently being updated.
                    Please try again a bit later or get in touch
                    with our dedicated customer support team to get
                    you unsubscribed.
                    Thank you for your understanding!"""
                )
                return redirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, 'marketing/subscribe.html', {
        'marketing_form': EmailForm(),
    })


mailchimp = Client()
mailchimp.set_config({
  'api_key': settings.MAILCHIMP_API_KEY,
  'server': settings.MAILCHIMP_REGION,
})


def mailchimp_ping_view(request):
    """
    Pings the Mailchimp API to check its connectivity and returns the response
    containing status information about the API.
    """
    response = mailchimp.ping.get()
    return JsonResponse(response)
