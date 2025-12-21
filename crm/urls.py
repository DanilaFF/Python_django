from django.urls import path
from . import views

app_name = "crm"

urlpatterns = [
    # Публичная бронь
    path("", views.public_reservation_create, name="home"),
    path("reserve/", views.public_reservation_create, name="public_reservation"),
    path("reserve/success/", views.reservation_success, name="reservation_success"),

    # 🔥 КАЛЕНДАРЬ БРОНИРОВАНИЙ (ТО, ЧЕГО НЕ ХВАТАЛО)
    path("crm/schedule/", views.reservation_schedule, name="reservation_schedule"),

    # Служебные разделы
    path("crm/", views.ReservationListView.as_view(), name="reservation_list"),
    path("crm/new/", views.ReservationCreateView.as_view(), name="reservation_new"),
    path("crm/cancel/<int:pk>/", views.cancel_reservation, name="reservation_cancel"),

    path("clients/", views.client_list, name="client_list"),
    path("clients/new/", views.client_create, name="client_create"),
]
