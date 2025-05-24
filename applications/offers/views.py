from rest_framework import generics, filters, serializers
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _
from applications.offers.models import Offer
from applications.offers.serializers import OfferSerializer
from applications.offers.choices.room_type import RoomType

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and
            request.user.role == "OWNER" and
            obj.owner == request.user
        )

class OfferListCreateView(generics.ListCreateAPIView):
    queryset = Offer.objects.filter(is_active=True).select_related('location', 'owner')
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, OrderingFilter]
    filterset_fields = {
        'location__city': ['exact', 'icontains'],
        'location__district': ['exact', 'icontains'],
        'price': ['gte', 'lte', 'exact'],
        'rooms_count': ['exact'],
    }
    search_fields = ['title', 'description', 'location__city', 'location__district']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        room_type_label = self.request.query_params.get('room_type')

        if room_type_label:
            room_type_value = RoomType.get_varname_by_value(room_type_label)
            queryset = queryset.filter(room_type=room_type_value) if room_type_value else queryset.none()

        return queryset

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated or self.request.user.role != "OWNER":
            raise serializers.ValidationError(_("Только арендодатели могут создавать объявления."))
        serializer.save(owner=self.request.user)

class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all().select_related('location', 'owner')
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsOwner()]
        return super().get_permissions()

    def perform_update(self, serializer):
        if not self.request.user.is_authenticated or self.request.user.role != "OWNER":
            raise serializers.ValidationError(_("Только арендодатели могут редактировать объявления."))
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.is_authenticated or self.request.user.role != "OWNER":
            raise serializers.ValidationError(_("Только арендодатели могут удалять объявления."))
        instance.delete()

class OfferToggleStatusView(generics.GenericAPIView):
    queryset = Offer.objects.only('id', 'is_active')
    serializer_class = OfferSerializer
    permission_classes = [IsOwner]

    def post(self, request, *args, **kwargs):
        offer = self.get_object()
        offer.is_active = not offer.is_active
        offer.save()
        return Response({
            'status': 'success',
            'is_active': offer.is_active,
            'message': _("Объявление {}.").format(
                _("активировано") if offer.is_active else _("деактивировано")
            )
        })


class MyOffersView(generics.ListAPIView):
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Offer.objects.filter(owner=self.request.user).select_related('location', 'owner')