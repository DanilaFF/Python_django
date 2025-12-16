from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Reservation


class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'crm/reservation_list.html'
    context_object_name = 'reservations'
    ordering = ['-date', '-start_time']

