from rest_framework import generics, filters
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework.response import Response

from applications.offers.models import Offer
from applications.bookings.models import Booking, BookingStatus
from applications.search.models import SearchQuery
from applications.search.serializers import SearchResultSerializer
from django.utils.translation import gettext_lazy as _

class SearchListView(generics.ListAPIView):
    queryset = Offer.objects.filter(is_active=True).select_related('location', 'owner')
    serializer_class = SearchResultSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, OrderingFilter]
    filterset_fields = {
        'location__city': ['exact', 'icontains'],
        'location__district': ['exact', 'icontains'],
        'price': ['gte', 'lte', 'exact'],
        'rooms_count': ['exact', 'gte', 'lte'],
        'room_type': ['exact'],
    }
    search_fields = ['title', 'description', 'location__city', 'location__district']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.query_params.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(location__city__icontains=query) |
                Q(location__district__icontains=query)
            )
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            booked_offers = Booking.objects.filter(
                status=BookingStatus.CONFIRMED,
                start_date__lte=end_date,
                end_date__gte=start_date
            ).values_list('offer_id', flat=True)
            queryset = queryset.exclude(id__in=booked_offers)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        query = request.query_params.get('q')
        city = request.query_params.get('location__city')
        district = request.query_params.get('district')
        min_price = request.query_params.get('price__gte')
        max_price = request.query_params.get('price__lte')
        rooms_count = request.query_params.get('rooms_count')
        room_type = request.query_params.get('room_type')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        ordering = request.query_params.get('ordering')
        if request.user.is_authenticated or query or any(
            [city, district, min_price, max_price, rooms_count, room_type, start_date, end_date]
        ):
            filters = {
                'city': city,
                'district': district,
                'min_price': min_price,
                'max_price': max_price,
                'rooms_count': rooms_count,
                'room_type': room_type,
                'start_date': start_date,
                'end_date': end_date,
                'ordering': ordering
            }
            search_query = SearchQuery(
                user=request.user if request.user.is_authenticated else None,
                query=query or ''
            )
            search_query.set_filters({k: v for k, v in filters.items() if v})
            search_query.save()
        return Response(serializer.data)