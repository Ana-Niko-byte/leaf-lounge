from django import forms
from .models import *


class OrderForm(forms.ModelForm):
    """
    A form for users to place book orders from the basket.

    This form is accessed after clicking 'SEcure Checkout' in the basket tab.

    This is a model-based form from the Order model, including the 'full_name',
    'email', 'phone_number', 'street_1', 'street_2', 'town_city', 'postcode',
    'country', and 'county' fields.

    UIUX:
    1. Autofocus placed inside the first field on load - 'full_name'
    2. Placeholders inserted into the relevant form fields.
    3. 'stripe-style-input' class applied to form fields.
    4. Labels removed from form fields and replaced with fieldsets in template.
    """
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
        placeholders = {
            'full_name': 'Evie Woods',
            'email': 'e.woods@example.com',
            'phone_number': '123 456 7890',
            'street_1': 'Street Address 1',
            'street_2': 'Street Address 2',
            'town_city': 'Town/City',
            'postcode': 'xxxxx',
            'county': 'County/State/Region',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
