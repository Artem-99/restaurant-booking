from django.db import models


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

    def __str__(self):
        return f"Столик №{self.number}"
