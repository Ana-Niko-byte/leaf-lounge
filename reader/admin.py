from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import *


@admin.register(UserProfile)
class UserProfileAdmin(SummernoteModelAdmin):
    list_display = ('user',)
