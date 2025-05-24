from django.contrib import admin
from .models import Location
from .model_reviews import Review

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'city', 'district', 'street', 'postal_code', 'country')
    search_fields = ('city', 'district', 'street', 'postal_code')
    list_filter = ('city', 'country')
    list_per_page = 10



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'offer', 'rating', 'comment', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('author__username', 'offer__title', 'comment')
    readonly_fields = ('created_at', 'updated_at')
