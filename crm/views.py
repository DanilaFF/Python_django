from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date

from .models import Client, Reservation
from .forms import ReservationForm, ClientForm, PublicReservationForm


# ---------- ПУБЛИЧНАЯ ЧАСТЬ ----------

def public_reservation_create(request):
    if request.method == "POST":
        form = PublicReservationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone"]
            name = form.cleaned_data["name"]

            client, created = Client.objects.get_or_create(
                phone=phone,
                defaults={"name": name},
            )

            if not created and client.name != name:
                client.name = name
                client.save(update_fields=["name"])

            reservation = form.save(commit=False)
            reservation.client = client
            reservation.save()

            return redirect("crm:reservation_success")
    else:
        form = PublicReservationForm()

    return render(request, "crm/reservation_form.html", {"form": form})


def reservation_success(request):
    return render(request, "crm/reservation_success.html")


# ---------- РАСПИСАНИЕ БРОНИРОВАНИЙ (КАЛЕНДАРЬ) ----------

@login_required
def reservation_schedule(request):
    selected_date = request.GET.get("date")
    if selected_date:
        selected_date = parse_date(selected_date)
    else:
        selected_date = date.today()

    reservations = (
        Reservation.objects
        .filter(date=selected_date)
        .select_related("client")
        .order_by("table_number", "start_time")
    )

    tables = {}
    for r in reservations:
        tables.setdefault(r.table_number, []).append(r)

    return render(
        request,
        "crm/reservation_schedule.html",
        {
            "selected_date": selected_date,
            "tables": tables,
        },
    )


# ---------- ЗАКРЫТАЯ ЧАСТЬ ----------

class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = "crm/reservation_list.html"
    context_object_name = "reservations"
    ordering = ["-date", "-start_time"]


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = "crm/reservation_form.html"
    success_url = reverse_lazy("crm:reservation_list")


@login_required
def cancel_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    reservation.status = Reservation.STATUS_CANCELED
    reservation.save(update_fields=["status"])
    return redirect("crm:reservation_list")


@login_required
def client_list(request):
    q = (request.GET.get("q") or "").strip()
    clients = Client.objects.all().order_by("name")
    if q:
        clients = clients.filter(Q(name__icontains=q) | Q(phone__icontains=q))
    return render(
        request,
        "crm/client_list.html",
        {"clients": clients, "q": q},
    )


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
