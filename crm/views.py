from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Reservation
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import ReservationForm



class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'crm/reservation_list.html'
    context_object_name = 'reservations'
    ordering = ['-date', '-start_time']

class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = "crm/reservation_form.html"
    success_url = reverse_lazy("crm:reservation_list")
