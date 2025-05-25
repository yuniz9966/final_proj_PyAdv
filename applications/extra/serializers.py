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
        user = request.user
        offer = data.get('offer')
        rating = data.get('rating')

        if user.role != 'RENTER':
            raise serializers.ValidationError(_("Только арендаторы могут оставлять отзывы."))

        if rating is not None and (rating < 1 or rating > 5):
            raise serializers.ValidationError(_("Рейтинг должен быть от 1 до 5."))

        # Проверка наличия подтверждённого бронирования
        from applications.bookings.models import Booking, BookingStatus
        if not Booking.objects.filter(
            renter=user,
            offer=offer,
            status=BookingStatus.CONFIRMED
        ).exists():
            raise serializers.ValidationError(_("Вы можете оставить отзыв только для забронированного жилья."))

        # Один отзыв на одно жилье
        if Review.objects.filter(offer=offer, author=user).exists():
            raise serializers.ValidationError(_("Вы уже оставили отзыв для этого предложения."))

        return data

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
