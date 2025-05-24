from rest_framework import serializers
from applications.extra.model_reviews import Review
from applications.offers.models import Offer
from applications.offers.serializers import OfferSerializer
from applications.user.serializers import UserSerializer
from django.utils.translation import gettext_lazy as _

class ReviewSerializer(serializers.ModelSerializer):
    offer = OfferSerializer(read_only=True)
    offer_id = serializers.PrimaryKeyRelatedField(
        queryset=Offer.objects.filter(is_active=True),
        source='offer',
        write_only=True
    )
    author = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'offer', 'offer_id', 'author', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']

    def validate(self, data):
        request = self.context['request']
        if request.user.role != 'RENTER':
            raise serializers.ValidationError(
                _("Только арендаторы могут оставлять отзывы.")
            )
        return data

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)