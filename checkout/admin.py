from django.contrib import admin
from .models import *


class BookLineItemAdminInline(admin.TabularInline):
    model = BookLineItem
    readonly_fields = ('order', 'book_order_cost',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (BookLineItemAdminInline,)
    readonly_fields = (
        'order_number',
        'date',
        'delivery_cost',
        'order_total',
        'grand_total'
    )
    fields = (
        'order_number',
        'date',
        'full_name',
        'email',
        'phone_number',
        'country',
        'postcode',
        'town_city',
        'street_1',
        'street_2',
        'county',
        'delivery_cost',
        'order_total',
        'grand_total',
    )
    list_display = (
        'order_number',
        'date',
        'full_name',
        'order_total',
        'grand_total',
    )
    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
