from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ClientForm
from .models import Client


@login_required
def client_list(request):
    q = request.GET.get("q", "").strip()
    clients = Client.objects.all().order_by("name")

    if q:
        clients = clients.filter(name__icontains=q) | clients.filter(phone__icontains=q)

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


from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render

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
