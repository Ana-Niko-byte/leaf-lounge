from django import forms


SUBJECTS = (
    ('GE', 'General Enquiry'),
    ('CS', 'Customer Support'),
    ('TS', 'Technical Support'),
    ('BP', 'Billing & Payments'),
    ('CO', 'Career Opportunities'),
    ('C', 'Complaint'),
    ('O', 'Other'),
)


class ContactForm(forms.Form):
    """
    A Contact form model for the Contact Page.

    Fields:
    name : textinput - the sender's name
    email : emailinput - the sender's email.
    subject : selectfield - the message subject.
    message : textarea - the sender's message.
    """
    name = forms.CharField(
        label='Name: ',
        widget=forms.TextInput(
            attrs={'placeholder': 'Emily Brontë', 'autofocus' : True}
        )
    )
    email = forms.EmailField(
        label='Email Address: ',
        widget=forms.EmailInput(
            attrs={'placeholder': 'e.bronte@example.com'}
        )
    )
    subject = forms.ChoiceField(
        label='Subject: ',
        choices=SUBJECTS,
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )
    message = forms.CharField(
        label='Message (max 400 characters): ',
        max_length=400,
        widget=forms.Textarea(
            attrs={
                'placeholder': '''Please tell us your life story in 400
                characters or less...'''
            }
        )
    )
