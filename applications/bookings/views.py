from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from applications.bookings.models import Booking, BookingStatus
from applications.bookings.serializers import BookingSerializer
from rest_framework.views import APIView
from rest_framework import status
from datetime import date

class IsRenter(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'RENTER'

    def has_object_permission(self, request, view, obj):
        return obj.renter == request.user

class IsOfferOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and
            request.user.role == 'OWNER' and
            obj.offer and
            obj.offer.owner == request.user
        )


class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all().select_related('offer__location', 'renter', 'offer__owner')
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['offer__id', 'renter__id', 'status', 'start_date', 'end_date']
    search_fields = ['offer__title', 'offer__description']

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Booking.objects.none()
        if user.role == 'RENTER':
            return Booking.objects.filter(renter=user).select_related('offer__location', 'renter', 'offer__owner')
        if user.role == 'OWNER':
            return Booking.objects.filter(offer__owner=user).select_related('offer__location', 'renter', 'offer__owner')
        return Booking.objects.none()

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated or self.request.user.role != 'RENTER':
            raise ValidationError(
                _("Только арендаторы могут создавать бронирования.")
            )
        serializer.save(renter=self.request.user)

class BookingDetailView(generics.RetrieveAPIView):  # Убрали Update и Destroy
    queryset = Booking.objects.all().select_related('offer__location', 'renter', 'offer__owner')
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookingCancelView(APIView):
    permission_classes = [IsRenter]

    def post(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, renter=request.user)
        except Booking.DoesNotExist:
            raise ValidationError(_('Бронирование не найдено'))

        if booking.status not in [BookingStatus.PENDING, BookingStatus.CONFIRMED]:
            raise ValidationError(_('Бронирование нельзя отменить'))

        if booking.start_date <= date.today():
            raise ValidationError(_('Срок отмены истёк'))

        booking.status = BookingStatus.CANCELLED
        booking.save()
        return Response(
            {'status': 'success', 'message': _('Бронирование отменено'), 'booking_status': booking.status},
            status=status.HTTP_200_OK
        )


class BookingStatusView(generics.GenericAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsOfferOwner]

    def post(self, request, *args, **kwargs):
        booking = self.get_object()
        action = request.data.get('action')

        if booking.status != BookingStatus.PENDING:
            raise ValidationError(
                _("Только бронирования в статусе 'Ожидает' можно подтвердить или отклонить.")
            )

        if action == 'confirm':
            booking.status = BookingStatus.CONFIRMED
            message = _("Бронирование подтверждено.")
        elif action == 'reject':
            booking.status = BookingStatus.REJECTED
            message = _("Бронирование отклонено.")
        else:
            raise ValidationError(_("Укажите действие: 'confirm' или 'reject'."))

        booking.save()

        return Response({
            'status': 'success',
            'message': message,
            'booking_status': booking.status
        })
