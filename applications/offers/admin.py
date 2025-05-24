from django.contrib import admin
from applications.offers.models import Offer


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'room_type_display', 'price', 'location', 'is_active', 'created_at')
    list_filter = ('room_type', 'is_active', 'location__city')
    search_fields = ('title', 'description', 'location__city', 'location__district')
    list_per_page = 10

    def room_type_display(self, obj):
        return obj.room_type if obj.room_type else '–'
    room_type_display.short_description = 'Room Type'