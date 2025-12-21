from django.urls import path
from . import views

app_name = "crm"

urlpatterns = [
    # Публичная часть
    path("", views.public_reservation_create, name="public_reservation"),
    path("success/", views.reservation_success, name="reservation_success"),

    # Закрытая часть (только по логину)
    path("reservations/", views.reservation_list, name="reservation_list"),
    path("reservations/new/", views.reservation_create, name="reservation_new"),
    path("reservations/<int:pk>/cancel/", views.cancel_reservation, name="cancel_reservation"),

    path("schedule/", views.reservation_schedule, name="reservation_schedule"),

    path("clients/", views.client_list, name="client_list"),
    path("clients/new/", views.client_create, name="client_create"),
]
