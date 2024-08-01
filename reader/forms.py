from django import forms

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
            self.fields[field].label = False
