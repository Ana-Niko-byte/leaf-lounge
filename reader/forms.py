from django import forms
from .widgets import CustomClearableFileInput

from library.models import Review
from .models import *


class UserProfileForm(forms.ModelForm):
    """
    A form for users to create a user profile. Each user can only
    have one user profile per account. In some cases, the user profile
    is created automatically.

    This is a model-based form from the UserProfile model, excluding
    the 'user' field.
    """
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
        Sets placeholders, removes labels, and applies a
        custom class to each form field.
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_street_1': 'Street Address 1',
            'default_street_2': 'Street Address 2',
            'default_town_city': 'Town or City',
            'default_postcode': 'Post Code',
            'default_county': 'County/State/Region',
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
    A form for users to leave reviews on purchased books. Reviews are tied
    to the user's user profile, and can be viewed under
    'My Profile' > 'My Reviews'.

    Each review requires approval prior to being displayed in the relevant book
    detail page. Unapproved reviews can be edited. All reviews can be deleted.

    This is a model-based form from the Review model, including the 'book',
    'title', 'rating', and 'comment' fields.
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
        Sets placeholders to the comment and rating fields, and
        adds a custom class to all fields.
        """
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if field == 'comment':
                self.fields[field].widget.attrs['placeholder'] = 'Great book!'
            elif field == 'rating':
                self.fields[field].widget.attrs['placeholder'] = '(Out of 10)'
            self.fields[field].widget.attrs['class'] = 'custom-fields'
