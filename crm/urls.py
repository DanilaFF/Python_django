from django.urls import path
from .views import ReservationListView

app_name = 'crm'

urlpatterns = [
    path('', ReservationListView.as_view(), name='reservation_list'),
]

