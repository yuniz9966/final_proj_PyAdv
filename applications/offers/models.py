from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from applications.extra.models import Location
from applications.user.models import User
from applications.offers.choices.room_type import RoomType


class Offer(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rooms_count = models.PositiveSmallIntegerField()
    room_type = models.CharField(max_length=50, choices=RoomType.choices())
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.room_type == RoomType.STUDIO and self.rooms_count > 1:
            raise ValidationError(_("Студия не может иметь больше одной комнаты."))

    class Meta:
        indexes = [
            models.Index(fields=['price']),
            models.Index(fields=['room_type']),
            models.Index(fields=['rooms_count']),
            models.Index(fields=['location']),
        ]

    def __str__(self):
        return self.title
