from django import forms
from .widgets import CustomClearableFileInput
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

    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    field_order = [
        'book',
        'rating',
        'comment',
    ]
