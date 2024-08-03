from django.contrib import admin

from reader.models import UserProfile
from .models import *


class CommunityAdmin(admin.ModelAdmin):
    fields = '__all__'
    readonly_fields = ('community')

admin.site.register(Community)