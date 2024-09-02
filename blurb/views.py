from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages

from django.conf import settings

from .forms import *

def blurb(request):
    return render(
        request,
        'blurb/index.html'
    )


def contact(request):
    """
    A view for handling post requests from the Contact page.
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
                '''Your message has been forwarded onto our team! We
                endeavour to respond within 2 business days :)'''
            )
            return redirect('home')
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
