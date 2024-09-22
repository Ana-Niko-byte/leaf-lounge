from django import forms


SUBJECTS = (
    ('General Enquiry', 'General Enquiry'),
    ('Customer Support', 'Customer Support'),
    ('Technical Support', 'Technical Support'),
    ('Billing & Payments', 'Billing & Payments'),
    ('Career Opportunities', 'Career Opportunities'),
    ('Complaint', 'Complaint'),
    ('Other', 'Other'),
)


class ContactForm(forms.Form):
    """
    A form for users to send queries to the Leaf Lounge team.

    This form is accessible under the `Contact` tab in the main navigation bar,
    as well as under the 'My Profile' > 'Need Help?' tabs.

    Fields:
    name : textinput - the sender's name
    email : emailinput - the sender's email.
    subject : selectfield - the message subject.
    message : textarea - the sender's message.
    """
    name = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Emily Brontë',
                'autofocus': True,
                'class': 'custom-fields',
                'aria-label': 'Name'
            }
        )
    )
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'e.bronte@example.com',
                'class': 'custom-fields',
                'aria-label': 'Email'
            }
        )
    )
    subject = forms.ChoiceField(
        label='',
        choices=SUBJECTS,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'class': 'custom-fields',
                'aria-label': 'Subject'
            }
        )
    )
    message = forms.CharField(
        label='',
        max_length=400,
        widget=forms.Textarea(
            attrs={
                'placeholder': '''Your query in 400 characters or less...''',
                'class': 'custom-fields-large',
                'aria-label': 'Message'
            }
        )
    )
