from django import forms


class EmailForm(forms.Form):
    """
    A form for users to subscribe to the Leaf Lounge Newsletter
    powered by MailChimp.

    This form is accessible in the footer of all pages.

    Fields:
    email : EmailField - the email input field.
    """
    email = forms.EmailField(max_length=128)

    def __init__(self, *args, **kwargs):
        """
        Sets a placeholder to the email field, sets a
        custom class and removes the label.
        """
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['email'].widget.attrs['class'] = 'subscribe-input'
        self.fields['email'].label = False
