from django.contrib import admin

from .models import *


class CommunityAdmin(admin.ModelAdmin):
    fields = '__all__'
    readonly_fields = ('community')


class ForumAdmin(admin.ModelAdmin):
    fields = '__all__'


class MessageAdmin(admin.ModelAdmin):
    fields = '__all__'
    readonly_fields = ('messenger')


admin.site.register(Community)
admin.site.register(Forum)
admin.site.register(Message)
