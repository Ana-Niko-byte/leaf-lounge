from django import forms


class EmailForm(forms.Form):
    email = forms.EmailField(max_length=128)

    def __init__(self, *args, **kwargs):
        """
        Set placeholders to each form field.
        Remove labels from fields.
        Set first field with autofocus.
        """
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['email'].widget.attrs['class'] = 'subscribe-input'
        self.fields['email'].label = False
