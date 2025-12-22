from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import PublicReservationForm, ReservationForm, ClientForm
from .models import Client, Reservation


def public_reservation_create(request):
    """Публичная бронь без логина: создаёт клиента, если его нет."""
    if request.method == "POST":
        form = PublicReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("crm:reservation_success")
    else:
        form = PublicReservationForm()

    return render(request, "crm/reservation_form.html", {"form": form, "back_url": None})


def reservation_success(request):
    return render(request, "crm/reservation_success.html")


@login_required
def reservation_list(request):
    reservations = Reservation.objects.select_related("client").order_by("-date", "-start_time", "-created_at")
    return render(request, "crm/reservation_list.html", {"reservations": reservations})


@login_required
def reservation_create(request):
    """Создание брони в закрытой части для кафе"""
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("crm:reservation_list")
    else:
        form = ReservationForm()

    return render(request, "crm/reservation_form.html", {"form": form, "back_url": reverse("crm:reservation_list")})


@login_required
def cancel_reservation(request, pk: int):
    """Отмена брони"""
    r = get_object_or_404(Reservation, pk=pk)
    r.status = Reservation.STATUS_CANCELED
    r.save(update_fields=["status"])

    # возвращаемся туда, откуда пришли
    return redirect(request.META.get("HTTP_REFERER") or "crm:reservation_list")


@login_required
def reservation_schedule(request):
    """Брони по дням + возможность отменять"""
    date_str = request.GET.get("date")
    selected_date = None

    if date_str:
        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            selected_date = None

    qs = Reservation.objects.select_related("client")
    if selected_date:
        qs = qs.filter(date=selected_date)

    qs = qs.order_by("table_number", "start_time")

    schedule = {}
    for r in qs:
        schedule.setdefault(r.table_number, []).append(r)

    return render(
        request,
        "crm/reservation_schedule.html",
        {"schedule": schedule, "selected_date": selected_date},
    )


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

    return render(request, "crm/client_form.html", {"form": form, "back_url": reverse("crm:client_list")})
