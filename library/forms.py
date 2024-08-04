from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    """
    A class for the book review form.
    """
    class Meta:
        model = Review
        fields = {
            'book',
            'rating',
            'comment',
        }

    field_order = [
        'book',
        'rating',
        'comment',
    ]
