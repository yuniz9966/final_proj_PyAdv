from django.db import models
from django.utils.translation import gettext_lazy as _
import json

class SearchQuery(models.Model):
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='search_queries'
    )
    query = models.CharField(max_length=255, blank=True)
    filters = models.TextField(default='{}')  # Храним JSON как строку
    created_at = models.DateTimeField(auto_now_add=True)

    def get_filters(self):
        """Десериализация JSON из строки."""
        return json.loads(self.filters)

    def set_filters(self, value):
        """Сериализация словаря в JSON-строку."""
        self.filters = json.dumps(value, ensure_ascii=False)

    def __str__(self):
        return f"Поиск: {self.query} от {self.user.username if self.user else 'Аноним'}"

    class Meta:
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['query']),
        ]