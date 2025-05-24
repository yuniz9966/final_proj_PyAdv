from rest_framework import serializers
from applications.search.models import SearchQuery
from applications.offers.serializers import OfferSerializer

class SearchQuerySerializer(serializers.ModelSerializer):
    filters = serializers.JSONField()  # Для корректной обработки JSON

    class Meta:
        model = SearchQuery
        fields = ['id', 'user', 'query', 'filters', 'created_at']

class SearchResultSerializer(OfferSerializer):
    class Meta(OfferSerializer.Meta):
        fields = OfferSerializer.Meta.fields