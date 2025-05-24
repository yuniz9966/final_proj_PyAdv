# applications/search/admin.py
from django.contrib import admin
from .models import SearchQuery
import json


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ('query', 'user', 'created_at', 'filters_display')
    list_filter = ('user', 'created_at')
    search_fields = ('query', 'user__username')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'filters_display')

    def filters_display(self, obj):
        try:
            filters = obj.get_filters()
            return json.dumps(filters, indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            return f"Невалидный JSON: {obj.filters}"

    filters_display.short_description = 'Фильтры'