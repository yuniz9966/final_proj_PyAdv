from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('renter', 'offer', 'start_date', 'end_date', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('renter__username', 'offer__title')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')