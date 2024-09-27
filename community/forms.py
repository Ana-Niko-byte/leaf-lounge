from django import forms
from library.models import *
from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class AuthorForm(forms.ModelForm):
    """
    A form for users to register as Leaf Lounge Authors.
    This form is accessible under the `Become an Auhor tab`.
    This is a model-based form from the Author model, including
    the 'first_name', 'last_name', 'd_o_b', 'nationality', and 'bio'
    fields.

    The d_o_b field is rendered as a dateinput, with relevant
    validation applied within views.py.
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
            'd_o_b': DateInput(attrs={'type': 'date'})
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
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'd_o_b': 'Date of Birth',
            'nationality': 'Nationality',
            'bio': 'Tell us a bit about yourself...',
        }

        self.fields['first_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            self.fields[field].widget.attrs[
                'placeholder'
            ] = placeholders.get(field, '')
            self.fields[field].label = False
            if field != 'bio':
                self.fields[field].widget.attrs['class'] = 'custom-fields'


class BookForm(forms.ModelForm):
    """
    A form for users to register their books after registering
    as Leaf Lounge authors using the AuthorForm above.
    This form is accessible under the `Become an Auhor tab` after
    completing the initial registration.
    This is a model-based form from the Book model, excluding
    the 'slug', 'rating', 'and author' fields.

    The 'slug' field is generated automatically when the book instance
    is created and saved. The 'rating' is user-based and is added dynamically
    via the ReviewForm (library app). The 'author' field is tied to the current
    user's UserProfile and is assigned automatically.
    """
    class Meta:
        model = Book
        exclude = {'slug', 'rating', 'author'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'title': 'Title',
            'isbn': 'ISBN',
            'blurb': 'Your Blurb',
            'year_published': 'Year Published',
            'publisher': 'Publisher',
            'type': 'Cover Type',
            'price': 'Price / Book',
        }

        self.fields['title'].widget.attrs['autofocus'] = True
        for field in self.fields:
            self.fields[field].widget.attrs[
                'placeholder'
            ] = placeholders.get(field, '')
            self.fields[field].label = False
            if field != 'blurb':
                self.fields[field].widget.attrs['class'] = 'custom-fields'


class ForumForm(forms.ModelForm):
    """
    A form for users to create a new community Forum. These forums
    belong to one community at a time, may share names, and all users
    inside a given community have the same access rights to each forum.

    This is a model-based form from the Forum model with a single field
    of 'name'. Post-save, a unique slug is generated for each model instance.
    """
    class Meta:
        model = Forum
        fields = {
            'name'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['autofocus'] = True
        self.fields['name'].label = False
        self.fields['name'].widget.attrs['placeholder'] = 'Descriptive Name: '
        self.fields['name'].widget.attrs['class'] = 'forum-input'
        self.fields['name'].widget.attrs['maxlength'] = '50'


class MessageForm(forms.ModelForm):
    """
    A form for Forum messages. This form allows users to send messages
    inside forums.

    This is a model-based form from the Message model with a single
    field of 'content'.
    """
    class Meta:
        model = Message
        fields = {
           'content'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['content'].widget.attrs['autofocus'] = True
        self.fields['content'].widget.attrs['class'] = 'forum-message-input'
        self.fields['content'].label = False
