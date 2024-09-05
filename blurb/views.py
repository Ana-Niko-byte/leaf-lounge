from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages

from django.conf import settings

from .forms import *


def blurb(request):
    """
    Retrieves and displays the details of the home page.
    """
    return render(
        request,
        'blurb/index.html'
    )


def contact(request):
    """
    This view is responsible for handling the posting of queries to the Leaf
    Lounge company and sender's email.

    ContactForm POST Data:
    name - the query sender's name.
    email - the query sender's email.
    subject - the option selected from the subject dropdown.
    message - the query message content.
    recipient_list - the Leaf Lounge email (personal email), and the query
    sender's email.

    Returns:
    HttpResponseRedirect: (successful request) Redirects the user to the home
    page with a success message.
    Render: (unsuccessful request) Renders the contact form with an error
    message.
    """

    if request.method == 'POST':
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            name = contact_form.cleaned_data['name']
            email = contact_form.cleaned_data['email']
            subject = contact_form.cleaned_data['subject']
            message = contact_form.cleaned_data['message']
            recipient_list = [settings.EMAIL_HOST_USER, f'{email}']
            send_mail(
                subject=subject,
                message=message,
                from_email=email,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            messages.success(
                request,
                """Your message has been forwarded onto our team! We
                endeavour to respond within 2 business days :)"""
            )
            return redirect('home')
        else:
            messages.error(
                request,
                """
                We were unable to send your message.Please double check
                your information and try again. If the error persists,
                please reach out to us directly via email and we will get
                back to you within two business days.
                Thank you for your understanding!"""
            )
            return redirect('contact')
    else:
        contact_form = ContactForm()
        context = {
            'contact_form': contact_form
        }
        return render(
            request,
            'blurb/contact.html',
            context
        )
