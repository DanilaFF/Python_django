from django.urls import path
from . import views

app_name = "crm"

urlpatterns = [
    path("clients/", views.client_list, name="client_list"),
    path("clients/new/", views.client_create, name="client_create"),
]
