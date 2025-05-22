from django.contrib import admin
from applications.offers.models import Offer
from applications.extra.models import Location


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'room_type', 'price', 'location', 'is_active', 'created_at')
    list_filter = ('room_type', 'is_active', 'location__city')
    search_fields = ('title', 'description', 'location__city', 'location__district')