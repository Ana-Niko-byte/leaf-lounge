from django import forms
from library.models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class AuthorForm(forms.ModelForm):
    """
    A form class for registering user as an author.
    """
    class Meta:
        model = Author
        fields = {
            'first_name',
            'last_name',
            'd_o_b',
            'nationality',
            'bio'
        }
        widgets = {
            'd_o_b' : DateInput(attrs={'type' : 'date'})
        }
    
    field_order = [
        'first_name',
        'last_name',
        'd_o_b',
        'nationality',
        'bio'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'first_name' : 'First Name',
            'last_name' : 'Last Name',
            'd_o_b' : 'Date of Birth',
            'nationality' : 'Nationality',
            'bio' : 'Tell us a bit about yourself...',
        }

        self.fields['first_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = placeholders.get(field, '')
            self.fields[field].label = False