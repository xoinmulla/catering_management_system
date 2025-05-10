from django.contrib import admin
from .models import Client, Event, Menu, Order

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'email')

admin.site.register(Menu)
admin.site.register(Order)
