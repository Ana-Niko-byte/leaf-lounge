from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import reverse
from django_countries.fields import CountryField

from community.models import Community
from reader.models import UserProfile

# Model Tuples
from ._covers import COVERS


class Author(models.Model):
    """
    Represents a Leaf Lounge author. Authors can register new books on the
    website, with new books being saved under their UserProfile.

    Fields:
    user_profile : FK : UserProfile - represent's the author's account
    if they have one.
    first_name : CharField - represents the author's firstname.
    last_name : CharField - represents the author's lastname.
    d_o_b : DateField - represents the author's date of birth.
    nationality : CharField : choices - represents a selection field for the
    author's nationality.
    bio : TextField - represents the author's bio.

    Methods:
    def __str__() -> str : Returns (author's first name) (author's last name).
    """
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        # Not all authors need to have an account!
        null=True,
        blank=True,
        related_name='author_profile'
    )
    first_name = models.CharField(
        max_length=20,
        null=False,
        blank=False
    )
    last_name = models.CharField(
        max_length=20,
        null=False,
        blank=False
    )
    d_o_b = models.DateField(
        verbose_name='Birth Date',
        null=False,
        blank=False
    )
    nationality = CountryField(
        blank_label='Unknown Nationality',
        null=True,
        blank=True
    )
    bio = models.TextField(
        max_length=500,
        null=False,
        blank=False
    )

    def __str__(self):
        """
        Returns : (str) : '(author's first name) (author's last name)'.
        """
        return f'{self.first_name} {self.last_name}'


class Genre(models.Model):
    """
    Represents the breakdown of a book Genre. Each genre has an associated
    community, which is created at the same time as a new Genre is created.
    Each book registered on the app is given an associated Genre. After
    purchasing the book, the user gets access to the community associated with
    the genre.

    Fields:
    name : CharField - the genre name.
    community : FK : Community - the community belonging to the genre.

    Methods:
    def __str__() -> str : (genre name)
    """
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
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
    Represents a Book on Leaf Lounge. Books can be uploaded directly by admin,
    or registered on the website by registered Leaf Lounge authors.
    After selecting (clicking) on a book on the 'Library' page, users are taken
    into a detail view of that book. All books have associated reviews,
    genres, authors, and communities.

    Fields:
    title : CharField - the book title.
    isbn : CharField - the book's Internation Standard Book Number.
    slug : SlugField - the book slug (name-author fields).
    author : FK : Author - the author of the book.
    genre : CharField : choices - the book genre.
    blurb : TextField - the book blurb.
    year_published : IntegerField - the year the book was published.
    publisher : CharField - the book publisher.
    type : CharField - the book cover type.
    date_added : DateField - the date the book was added to the database.
    price : DecimalField - the book price.
    image : ImageField - the book cover image.

    Methods:
    def __str__() -> str :
    (author's firstname) (author's lastname) '"(book title)" by (book author)'.

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

    def get_absolute_url() :
    Returns the absolute url with the book 'slug' parameter (detail page).

    Meta:
        Orders by earliest date added.
    """
    COVERS = [
        ('SC', 'Softcover'),
        ('HB', 'Hardback'),
        ('D', 'Epub'),
    ]
    title = models.CharField(
        max_length=100
    )
    # Internation Standard Book Number - books after 2007 are 13 digits long.
    isbn = models.CharField(
        max_length=13
    )
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
    blurb = models.TextField(
        max_length=500
    )
    year_published = models.IntegerField(
        validators=[MaxValueValidator(2024)]
    )
    publisher = models.CharField(
        max_length=100
    )
    type = models.CharField(
        max_length=9,
        choices=COVERS,
        default='SC'
    )
    date_added = models.DateField(
        auto_now_add=True
    )
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )
    # placeholder for Cloudinary.
    image = models.ImageField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        """
        Returns -> str : '"(book title)" by (author)'.
        """
        return f'"{self.title}" by {self.author}'

    def save(self, *args, **kwargs):
        """
        Saves a custom url to the (self.slug) parameter as
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
    Represents a book review. Reviews can be left by registered users, who have
    purchased at least one book. The link for this is under the 'My Books' tab
    in the secondary navigation bar. Reviews can be edited prior to approval,
    and deleted at any stage. Approved reviews are displayed on the relevant
    book detail page. Reviews are displayed as star fillings on all relevant
    pages.

    Fields:
    reviewer : FK : User - the user leaving the review.
    book : FK : Book - the book being reviewed.
    title : CharField - the review title.
    rating : IntegerField - the book rating out of 10.
    comment : TextField - the user's verbal book rating.
    reviewed_on : DateField - the date the review was left on.
    approved : BooleanField - whether the comment is admin approved.
    """
    reviewer = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewer'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviewed_book'
    )
    title = models.CharField(
        max_length=80,
        null=False,
        blank=False
    )
    rating = models.IntegerField(
        validators=[
            MaxValueValidator(10), MinValueValidator(1)],
        null=False,
        blank=False
    )
    comment = models.TextField(
        max_length=500,
        null=False,
        blank=False
    )
    reviewed_on = models.DateField(
        auto_now_add=True,
        null=False,
        blank=False
    )
    approved = models.BooleanField(
        default=False
    )

    def __str__(self):
        """
        Returns -> str : '(book title) : (book rating)'.
        """
        return f'Review for {self.book} : {self.rating}/10'
