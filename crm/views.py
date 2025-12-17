from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Reservation
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import ReservationForm
from django.shortcuts import get_object_or_404, redirect

def cancel_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    reservation.status ="canceled"
    reservation.save()
    return redirect("crm:reservation_list")

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

from .forms import ClientForm
from .models import Client


@login_required
def client_list(request):
    q = (request.GET.get("q") or "").strip()
    clients = Client.objects.all().order_by("name")
    if q:
        clients = clients.filter(Q(name__icontains=q) | Q(phone__icontains=q))
    return render(request, "crm/client_list.html", {"clients": clients, "q": q})


@login_required
def client_create(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("crm:client_list")
    else:
        form = ClientForm()
    return render(request, "crm/client_form.html", {"form": form})

