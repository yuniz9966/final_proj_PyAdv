from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from applications.extra.model_reviews import Review
from applications.extra.serializers import ReviewSerializer
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all().select_related('offer', 'author')
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        offer_id = self.request.query_params.get('offer_id')
        if offer_id:
            return Review.objects.filter(offer_id=offer_id).select_related('offer', 'author')
        return Review.objects.none()

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated or self.request.user.role != 'RENTER':
            raise ValidationError(_("Только арендаторы могут создавать отзывы."))
        serializer.save(author=self.request.user)