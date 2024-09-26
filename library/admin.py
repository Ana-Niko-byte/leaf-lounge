from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import *


@admin.register(Author)
class AuthorAdmin(SummernoteModelAdmin):
    list_display = ('first_name', 'last_name', 'd_o_b')
    summernote_fields = ('bio',)
    ordering = ('last_name',)


@admin.register(Genre)
class GenreAdmin(SummernoteModelAdmin):
    list_display = ('name', 'community')


@admin.register(Book)
class BookAdmin(SummernoteModelAdmin):
    list_display = (
        'title',
        'genre',
        'author',
        'year_published',
        'publisher',
    )
    search_fields = [
        'title',
        'genre',
        'author',
        'author__last_name',
        'genre',
        'year_published',
        'publisher'
    ]
    list_filter = ('genre', 'year_published', 'publisher')
    summernote_fields = ('blurb',)
    ordering = ('date_added',)


@admin.register(Review)
class ReviewAdmin(SummernoteModelAdmin):
    fields = ('reviewer', 'book', 'rating', 'comment', 'approved')
    readonly_fields = ('reviewed_on',)
