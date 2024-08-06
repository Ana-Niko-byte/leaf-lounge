from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import reverse
from django_countries.fields import CountryField

from community.models import Community

# Model Tuples
from ._covers import COVERS


class Author(models.Model):
    """
    A class representing an author model.

    Fields:
    first_name : CharField - represents the author's firstname.
    last_name : CharField - represents the author's lastname.
    d_o_b : DateField - represents the author's date of birth.
    nationality : CharField : choices - represents a selection field for the
    author's nationality.
    bio : TextField - represents the author's bio.

    Methods:
    def __str__():
        Returns (author's first name) (author's last name).
    """
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    d_o_b = models.DateField(default='unknown', verbose_name='BirthDate')
    nationality = CountryField(blank_label='Unknown', null=True, blank=True)
    bio = models.TextField(max_length=500)

    def __str__(self):
        """
        Returns : (str) : '(author's first name) (author's last name)'.
        """
        return f'{self.first_name} {self.last_name}'


class Genre(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text='This field will be auto-filled after save.',
        related_name='genre_community'
    )

    def __str__(self):
        return f'{self.name}'


class Book(models.Model):
    """
    A class representing a book model.

    Fields:
    title : CharField - the book title.
    isbn : CharField - the book's Internation Standard Book Number.
    slug : SlugField - the book slug (name-author fields).
    author : FK : Author - the author of the book.
    genre : CharField : choices - the book genre.
    blurb : TextField - the book blurb.
    year_published : IntegerField - the year the book was published.
    publisher : CharField - the book publisher.
    rating : DecimalField - the book rating (out of 10).
    type : CharField - the book cover type.
    date_added : DateField - the date the book was added to the database.
    price : DecimalField - the book price.
    image : ImageField - the book cover image.

    Methods:
    def __str__():
        Returns : (str) : '"(book title)" by (book author)'.

    def save():
        try:
            Slug is saved automatically.
            Checks if the title of the book has been changed (if it no longer
            matches the one in the db).
            If true - re-saves the slug to match the new title-author
            concatenation.
        except Book.DoesNotExist:
            Catches the DoesNotExist error and saves the model as a new
            instance.

    def get_absolute_url():
        Returns the absolute url with the book 'slug' parameter (detail page).

    Meta:
        orders by earliest date added.
    """
    COVERS = [
        ('SC', 'Softcover'),
        ('HB', 'Hardback'),
        ('D', 'Epub'),
    ]
    title = models.CharField(max_length=100)
    # Internation Standard Book Number - books after 2007 are 13 digits long.
    isbn = models.CharField(max_length=13)
    # SlugField can be blank as slug is saved following model instance save.
    slug = models.SlugField(
        max_length=100,
        blank=True,
        null=True,
        help_text='This field will be auto-filled after save.'
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='author_books'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name='book_genre',
        null=True,
        blank=False
    )
    blurb = models.TextField(max_length=500)
    # Change to dynamic year later
    year_published = models.IntegerField(validators=[MaxValueValidator(2024)])
    publisher = models.CharField(max_length=100)
    rating = models.DecimalField(
        decimal_places=2,
        validators=[
            MinValueValidator(
                0.01,
                message='Rating cannot be lower than 0.01'
            ),
        ],
        max_digits=3,
    )
    type = models.CharField(max_length=9, choices=COVERS, default='SC')
    date_added = models.DateField(auto_now_add=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    # placeholder for Cloudinary.
    image = models.ImageField(null=True, blank=True)

    class Meta:
        """
        Orders books by last added.
        """
        ordering = ['-date_added']

    def __str__(self):
        """
        Returns : (str) : '"(book title)" by (author)'.
        """
        return f'"{self.title}" by {self.author}'

    def save(self, *args, **kwargs):
        """
        Saves a custom url to the (self.slug) parameter with
        (book title)-(author last name).

        Note : Done so in case books from different authors
        have the same title, thus omitting probability of url clashes.
        """
        try:
            # Slug is saved automatically.
            self.slug = slugify(self.title + '-' + self.author.last_name)
            if self.title != Book.objects.get(id=self.id).title:
                self.slug = slugify(self.title + '-' + self.author.last_name)
            super(Book, self).save(*args, **kwargs)
        except Book.DoesNotExist:
            super(Book, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Returns : the book detail page with (self.slug) as url argument.
        """
        return reverse('book-summary', args=[self.slug])

class Review(models.Model):
    """
    A class for a book review.

    Fields:
    reviewer : FK : User - the user leaving the review.
    book : FK : Book - the book being reviewed.
    rating : IntegerField - the book rating out of 10.
    comment : TextField - the user's verbal book rating.
    reviewed_on : DateField - the date the review was left on.
    approved : BooleanField - whether the comment is admin approved.
    """
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewer')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviewed_book')
    rating = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)], null=False, blank=False)
    comment = models.TextField(max_length=500, null=False, blank=False)
    reviewed_on = models.DateField(auto_now_add=True, null=False, blank=False)
    approved = models.BooleanField(default=False)