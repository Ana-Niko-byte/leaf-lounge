from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
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
        form = EmailForm(request.POST)
        if form.is_valid():
            try:
                form_email = form.cleaned_data['email']
                member_info = {
                    'email_address': form_email,
                    'status': 'subscribed',
                    'merge_fields': {
                        'FNAME': 'Elliot',
                        'LNAME': 'Alderson',
                    }
                }
                response = mailchimp.lists.add_list_member(
                    settings.MAILCHIMP_MARKETING_AUDIENCE_ID,
                    member_info,
                )
                return redirect('subscribe-success')

            except ApiClientError as error:
                return redirect('subscribe-fail')

    return render(request, 'marketing/subscribe.html', {
        'form': EmailForm(),
    })


def subscribe_success_view(request):
    """
    Renders the dedicated success page following successful subscription.
    """
    return render(
        request,
        'marketing/message.html',
        {
            'title': 'Successfully subscribed',
            'message': 'You\'ve successfully subscribed to our mailing list.',
        }
    )


def subscribe_fail_view(request):
    """
    Renders the dedicated fail page following unsuccessful subscription.
    """
    return render(
        request,
        'marketing/message.html',
        {
            'title': 'Failed to subscribe',
            'message': 'Oops, something went wrong.',
        }
    )


def unsubscribe_view(request):
    """
    Handles user UNsubscriptions by processing the subscription form with the
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
        form = EmailForm(request.POST)
        if form.is_valid():
            try:
                form_email = form.cleaned_data['email']
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
                return redirect('unsubscribe-success')

            except ApiClientError as error:
                return redirect('unsubscribe-fail')

    return render(request, 'marketing/unsubscribe.html', {
        'form': EmailForm(),
    })


def unsubscribe_success_view(request):
    """
    Renders the dedicated success page following successful unsubscription.
    """
    return render(
        request,
        'marketing/message.html',
        {
            'title': 'Successfully unsubscribed',
            'message': 'You\'ve unsubscribed from our mailing list.',
        }
    )


def unsubscribe_fail_view(request):
    """
    Renders the dedicated fail page following unsuccessful unsubscription.
    """
    return render(
        request,
        'marketing/message.html',
        {
            'title': 'Failed to unsubscribe',
            'message': 'Oops, something went wrong.',
        }
    )


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
