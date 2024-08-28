from django import forms
from .widgets import CustomClearableFileInput

from library.models import Review
from .models import *

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    field_order = [
        'street_1',
        'street_2',
        'town_city',
        'postcode',
        'country',
        'county',
    ]
    
    def __init__(self, *args, **kwargs):
        """
        Set placeholders to each form field.
        Remove labels from fields.
        Set first field with autofocus.
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number' : 'Phone Number',
            'default_street_1' : 'Street Address 1',
            'default_street_2' : 'Street Address 2',
            'default_town_city' : 'Town or City',
            'default_postcode' : 'Post Code',
            'default_county' : 'County/State/Region',
        }

        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
                self.fields[field].widget.attrs['class'] = 'custom-fields'
            self.fields[field].label = False


class ReviewForm(forms.ModelForm):
    """
    A class for the book review form.
    """
    class Meta:
        model = Review
        fields = {
            'book',
            'title',
            'rating',
            'comment',
        }

    field_order = [
        'book',
        'title',
        'rating',
        'comment',
    ]

    def __init__(self, *args, **kwargs):
        """
        Set placeholders to each form field.
        Remove labels from fields.
        Set first field with autofocus.
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'comment': 'Best book ever!',
        }

        for field in self.fields:
            if field == 'comment':
                self.fields[field].widget.attrs['placeholder'] = f'{placeholders[field]}'
            elif field == 'rating':
                self.fields[field].widget.attrs['placeholder'] = '(Out of 10)'
            self.fields[field].widget.attrs['class'] = 'custom-fields'