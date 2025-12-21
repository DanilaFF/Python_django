from django.contrib import admin
from .models import Client, Reservation


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone")
    search_fields = ("name", "phone")


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "client",
        "date",
        "start_time",
        "end_time",
        "table_number",
        "guests",
        "status",
        "created_at",
    )
    list_filter = ("date", "status")
