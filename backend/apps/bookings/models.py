from django.db import models
from django.conf import settings


class Booking(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = "confirmed", "Подтверждено"
        CANCELLED = "cancelled", "Отменено"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    table = models.ForeignKey(
        "tables.Table",
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    guests_count = models.IntegerField(default=1)
    comment = models.TextField(blank=True, default="")
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.CONFIRMED
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "bookings"
        ordering = ["-created_at"]
