from django.contrib import admin

from .models import *


class CommunityAdmin(admin.ModelAdmin):
    fields = '__all__'
    readonly_fields = ('community',)


class MessageAdminInline(admin.TabularInline):
    model = Message
    readonly_fields = ('messenger',)


class ForumAdmin(admin.ModelAdmin):
    inlines = (MessageAdminInline,)


admin.site.register(Community)
admin.site.register(Forum, ForumAdmin)
