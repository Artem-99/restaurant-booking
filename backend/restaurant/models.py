from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name"]

    class Meta:
        db_table = "users"


class Table(models.Model):
    number = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    location = models.CharField(max_length=100, default="Основной зал")
    description = models.TextField(blank=True, default="")
    is_available = models.BooleanField(default=True)

    class Meta:
        db_table = "tables"
        ordering = ["number"]


class Booking(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = "confirmed", "Подтверждено"
        CANCELLED = "cancelled", "Отменено"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings"
    )
    table = models.ForeignKey(
        Table, on_delete=models.CASCADE, related_name="bookings"
    )
    date = models.DateField()
    start_time = models.TimeField()
    guests_count = models.IntegerField(default=1)
    comment = models.TextField(blank=True, default="")
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.CONFIRMED
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "bookings"
        ordering = ["-created_at"]
