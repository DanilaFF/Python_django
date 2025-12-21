from django.db import models


class Client(models.Model):
    """Клиент кафе."""
    name = models.CharField("Имя", max_length=100)
    phone = models.CharField("Телефон", max_length=20)

    def __str__(self) -> str:
        return f"{self.name} ({self.phone})"


class Reservation(models.Model):
    """Бронь столика в кафе."""
    STATUS_BOOKED = "booked"
    STATUS_CANCELED = "canceled"
    STATUS_COMPLETED = "completed"

    STATUS_CHOICES = [
        (STATUS_BOOKED, "Забронировано"),
        (STATUS_CANCELED, "Отменено"),
        (STATUS_COMPLETED, "Завершено"),
    ]

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="reservations",
    )
    date = models.DateField("Дата")
    start_time = models.TimeField("Начало")
    end_time = models.TimeField("Конец")
    table_number = models.PositiveSmallIntegerField("Номер стола", default=1)
    guests = models.PositiveSmallIntegerField("Гостей", default=1)
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_BOOKED,
    )
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    def __str__(self) -> str:
        return f"Стол {self.table_number} {self.date} {self.start_time}-{self.end_time}"

    @property
    def time(self) -> str:
        st = self.start_time.strftime("%H:%M") if self.start_time else ""
        et = self.end_time.strftime("%H:%M") if self.end_time else ""
        return f"{st}–{et}".strip("–")

    @property
    def client_name(self) -> str:
        return self.client.name if self.client else ""
