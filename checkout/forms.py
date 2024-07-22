from django import forms

from .models import *

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = {
            'full_name',
            'email',
            'phone_number',
            'street_1',
            'street_2',
            'town_city',
            'postcode',
            'country',
            'county',
        }

    field_order = [
        'full_name',
        'email',
        'phone_number',
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
        # Define placeholders to go in fields.
        placeholders = {
            'full_name' : 'Evie Woods',
            'email' : 'e.woods@example.com',
            'phone_number' : '123 456 7890',
            'street_1' : 'Street Address 1',
            'street_2' : 'Street Address 2',
            'town_city' : 'Town/City',
            'postcode' : 'xxx xxxx',
            'country' : 'Country',
            'county' : 'County',
        }

        # Cursor in form on load.
        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            # Set defined placeholders to HTML 'placeholder' attribute.
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False