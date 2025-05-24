from rest_framework import serializers
from applications.offers.models import Offer
from applications.extra.models import Location
from applications.user.serializers import UserSerializer
from applications.offers.choices.room_type import RoomType
from django.utils.translation import gettext_lazy as _

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'city', 'district', 'street', 'postal_code', 'country', 'latitude', 'longitude']

class OfferSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    owner = UserSerializer(read_only=True)
    room_type = serializers.ChoiceField(choices=RoomType.choices())

    class Meta:
        model = Offer
        fields = [
            'id', 'title', 'description', 'location', 'price', 'rooms_count',
            'room_type', 'is_active', 'owner', 'created_at', 'updated_at'
        ]

    def get_room_type(self, obj):
        try:
            return dict(RoomType.choices())[obj.room_type]
        except KeyError:
            return None

    def validate(self, data):
        room_type = data.get('room_type')
        rooms_count = data.get('rooms_count')
        if room_type == RoomType.STUDIO and rooms_count > 1:
            raise serializers.ValidationError(
                _("Студия не может иметь больше одной комнаты.")
            )
        return data

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        location, _ = Location.objects.get_or_create(**location_data)
        offer = Offer.objects.create(location=location, **validated_data)
        return offer

    def update(self, instance, validated_data):
        location_data = validated_data.pop('location', None)
        if location_data:
            Location.objects.filter(id=instance.location.id).update(**location_data)
            instance.location.refresh_from_db()
        return super().update(instance, validated_data)