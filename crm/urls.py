from django.urls import path
from . import views

app_name = "crm"

urlpatterns = [
    path("", views.ReservationListView.as_view(), name="reservation_list"),
    path("new/", views.ReservationCreateView.as_view(), name="reservation_new"),
]


