from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.shortcuts import reverse

# Model Tuples
from ._nationalities import NATIONALITIES
from ._genres import GENRES
from ._covers import COVERS


class Author(models.Model):
    '''
    A class representing an author model.

    Attributes:
    first_name : CharField - represents the author's firstname.
    last_name : CharField - represents the author's lastname.
    d_o_b : DateField - represents the author's date of birth.
    nationality : CharField : choices - represents a selection field for the
    author's nationality.
    bio : TextField - represents the author's bio.

    Methods:
    def __str__():
        returns (author's first name) (author's last name)
    '''
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    d_o_b = models.DateField(default='unknown', verbose_name='BirthDate')
    nationality = models.CharField(choices=NATIONALITIES, max_length=30)
    bio = models.TextField(max_length=500)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):
    '''
    A class representing a book model.

    Attributes:
    title : CharField - the book title.
    isbn : CharField - the book's Internation Standard Book Number.
    slug : SlugField - the book slug (name-author fields).
    author : FK : Author - the author of the book.
    genre : CharField : choices - the book genre.
    blurb : TextField - the book blurb.
    year_published : IntegerField - the year the book was published.
    publisher : CharField - the book publisher.
    rating : DecimalField - the book rating (out of 10).
    date_added : DateField - the date the book was added to the database.
    price : DecimalField - the book price.
    image : ImageField - the book cover image. 

    Methods:
    def __str__():
        returns "(book title)" by (book author)

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
        Returns the absolute url with the book 'slug' paramter (detail page).

    Meta:
        orders by earliest date added.
    '''
    COVERS = [
        ('SC', 'Softcover'),
        ('HB', 'Hardback'),
        ('D', 'Epub'),
    ]
    title = models.CharField(max_length=100)
    # Internation Standard Book Number - all books after 2007 are 13 digits long.
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
    genre = models.CharField(choices=GENRES, max_length=50)
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
    # Add book type - softback/hardback/kindle after Stripe Payment completion.
    price = models.DecimalField(max_digits=5, decimal_places=2)
    # placeholder for Cloudinary.
    image = models.ImageField(null=True, blank=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return f'"{self.title}" by {self.author}'

    def save(self, *args, **kwargs):
        try:
            # Slug is saved automatically.
            self.slug = slugify(self.title + '-' + self.author.last_name)
            if self.title != Book.objects.get(id=self.id).title:
                self.slug = slugify(self.title + '-' + self.author.last_name)
            super(Book, self).save(*args, **kwargs)
        except Book.DoesNotExist:
            super(Book, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('book-summary', args=[self.slug])
