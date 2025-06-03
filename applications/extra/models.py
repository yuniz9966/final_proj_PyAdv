from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Location(models.Model):
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default="Germany")
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        parts = [self.city.strip()]
        if self.district and self.district.strip():
            parts.append(self.district.strip())
        if self.street and self.street.strip():
            parts.append(self.street.strip())
        return ", ".join(parts)

    class Meta:
        unique_together = ['city', 'district', 'street', 'postal_code']
        indexes = [
            models.Index(fields=['city']),
            models.Index(fields=['district']),
            models.Index(fields=['postal_code']),
        ]


    def clean(self):
        if not self.city.strip():
            raise ValidationError(_("City cannot be empty."))

    # def __str__(self):
    #     return f"{self.city}, {self.district}, {self.street}"
