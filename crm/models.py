from django.db import models
from datetime import time as dt_time


class Client(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return f'{self.name} ({self.phone})'


class Reservation(models.Model):
    STATUS_BOOKED, STATUS_CANCELED, STATUS_COMPLETED  = 'booked', 'canceled', 'completed'
    STATUS_CHOICES = [
        (STATUS_BOOKED, 'Забронировано'),
        (STATUS_CANCELED,'Отменено'),
        (STATUS_COMPLETED,'Завершено'),
    ]
    guests = models.PositiveSmallIntegerField("Гостей", default=1)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='reservations')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    table_number = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default=STATUS_BOOKED)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Стол {self.table_number} {self.date} {self.start_time}'

@property
def time(self):
    st = self.start_time.strftime("%H:%M") if self.start_time else ""
    et = self.end_time.strftime("%H:%M") if self.end_time else ""
    return f"{st}–{et}".strip("–")

@property
def client_name(self):
    return self.client.name if self.client else ""