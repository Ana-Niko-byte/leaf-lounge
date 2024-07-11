from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import *


@admin.register(Author)
class AuthorAdmin(SummernoteModelAdmin):
    list_display = ('first_name', 'last_name', 'd_o_b')
    summernote_fields = ('bio',)


@admin.register(Book)
class BookAdmin(SummernoteModelAdmin):
    list_display = ('title', 'author', 'year_published')
    search_fields = ['title', 'author', 'genre', 'year_published']
    list_filter = ('genre', 'year_published')
    summernote_fields = ('blurb',)