from django.db import models
from django.utils.text import slugify
from django.core.validators import MaxValueValidator

# Model Tuples
from ._nationalities import NATIONALITIES
from ._genres import GENRES


class Author(models.Model):
    '''
    A class representing an author model.

    Attributes:
    first_name : CharField - represents the author's firstname.
    last_name : CharField - represents the author's lastname.
    d_o_b : DateField - represents the author's date of birth.
    nationality : CharField : choices - represents a selection field for the
    author's nationality.
    books_published : FK : Book - represents the books published by the author.

    Methods:
    def __str__():
        returns (author's first name) (author's last name)
    '''
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    # Change to dynamic year - 10 years in case there are any child prodigies :P.
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
    slug : SlugField - the book slug (name-author fields).
    author : FK : Author - the author of the book.
    genre : CharField : choices - the book genre.
    blurb : TextField - the book blurb.
    year_published : IntegerField - the year the book was published.
    date_added : DateField - the date the book was added to the database.

    Methods:
    def __str__():
        returns "(book title)" by (book author)

    Meta:
        orders by earliest date added.
    '''
    title = models.CharField(max_length=100)
    # SlugField can be blank as the slug is saved following model instance save.
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
    date_added = models.DateField(auto_now_add=True)

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

