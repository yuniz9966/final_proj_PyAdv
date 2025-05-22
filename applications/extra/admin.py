from django.contrib import admin
from .models import Location

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'city', 'district', 'street', 'postal_code', 'country')
    search_fields = ('city', 'district', 'street', 'postal_code')
    list_filter = ('city', 'country')
