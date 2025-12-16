from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=40, blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return f"{self.name} ({self.phone})" if self.phone else self.name
