from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from marketing.forms import EmailForm


def subscribe_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            form_email = form.cleaned_data['email']
            # TODO: use Mailchimp API to subscribe
            return redirect('subscribe-success')

    return render(
        request,
        'marketing/subscribe.html',
        {
            'form': EmailForm(),
        }
    )


def subscribe_success_view(request):
    return render(
        request,
        'marketing/message.html',
        {
            'title': 'Successfully subscribed',
            'message': 'You\'ve successfully subscribed to our mailing list.',
        }
    )


def subscribe_fail_view(request):
    return render(
        request,
        'marketing/message.html',
        {
            'title': 'Failed to subscribe',
            'message': 'Oops, something went wrong.',
        }
    )


def unsubscribe_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            form_email = form.cleaned_data['email']
            # TODO: use Mailchimp API to unsubscribe
            return redirect('unsubscribe-success')

    return render(
        request,
        'marketing/unsubscribe.html',
        {
            'form': EmailForm(),
        }
    )


def unsubscribe_success_view(request):
    return render(
        request,
        'marketing/message.html',
        {
            'title': 'Successfully unsubscribed',
            'message': 'You\'ve unsubscribed from our mailing list.',
        }
    )


def unsubscribe_fail_view(request):
    return render(
        request,
        'marketing/message.html',
        {
            'title': 'Failed to unsubscribe',
            'message': 'Oops, something went wrong.',
        }
    )
