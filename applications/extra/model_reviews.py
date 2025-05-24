from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from applications.bookings.models import Booking, BookingStatus

class Review(models.Model):
    offer = models.ForeignKey(
        'offers.Offer',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('Предложение')
    )
    author = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('Автор')
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name=_('Рейтинг'),
        help_text=_('Оценка от 1 до 5')
    )
    comment = models.TextField(
        verbose_name=_('Отзыв'),
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Создано')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Обновлено')
    )

    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError(_('Рейтинг должен быть от 1 до 5.'))
        # Проверка, что автор имеет подтверждённое бронирование
        if not Booking.objects.filter(
            renter=self.author,
            offer=self.offer,
            status=BookingStatus.CONFIRMED
        ).exists():
            raise ValidationError(_('Вы можете оставить отзыв только для забронированного жилья.'))
        # Проверка, что пользователь не оставлял отзыв для этого предложения
        if Review.objects.filter(offer=self.offer, author=self.author).exclude(id=self.id).exists():
            raise ValidationError(_('Вы уже оставили отзыв для этого предложения.'))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
        indexes = [
            models.Index(fields=['offer']),
            models.Index(fields=['author']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.author.username} - {self.offer.title} ({self.rating})"