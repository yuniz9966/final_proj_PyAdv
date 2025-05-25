from datetime import date
from rest_framework import serializers
from applications.bookings.models import Booking, BookingStatus
from applications.offers.models import Offer
from applications.offers.serializers import OfferSerializer
from applications.user.serializers import UserSerializer
from django.utils.translation import gettext_lazy as _


class BookingSerializer(serializers.ModelSerializer):
    offer = OfferSerializer(read_only=True)
    offer_id = serializers.PrimaryKeyRelatedField(
        queryset=Offer.objects.filter(is_active=True),
        source='offer',
        write_only=True
    )
    renter = UserSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'offer', 'offer_id', 'renter',
            'start_date', 'end_date', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['renter', 'status', 'created_at', 'updated_at']

    def validate(self, data):
        renter = self.context['request'].user
        if renter.role != 'RENTER':
            raise serializers.ValidationError(
                _("Только арендаторы могут создавать бронирования.")
            )
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        if start_date and start_date < date.today():
            raise serializers.ValidationError(
                _("Дата начала должна быть в будущем.")
            )
        if end_date and start_date and end_date <= start_date:
            raise serializers.ValidationError(
                _("Дата окончания должна быть позже даты начала.")
            )
        return data

    def create(self, validated_data):
        validated_data['renter'] = self.context['request'].user
        return super().create(validated_data)