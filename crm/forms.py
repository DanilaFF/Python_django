from django import forms
from .models import Client, Reservation


class PublicReservationForm(forms.ModelForm):
    """
    Публичная форма бронирования:
    - Имя
    - Телефон
    - Дата/время
    - Стол
    - Гостей

    При сохранении:
    - если клиента нет -> создаём
    - если есть -> используем существующего
    """

    name = forms.CharField(
        label="Имя",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    phone = forms.CharField(
        label="Телефон",
        max_length=20,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "+7"}),
    )

    class Meta:
        model = Reservation
        fields = ("date", "start_time", "end_time", "table_number", "guests")
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "start_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "end_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "table_number": forms.NumberInput(attrs={"class": "form-control"}),
            "guests": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned = super().clean()
        st = cleaned.get("start_time")
        et = cleaned.get("end_time")
        if st and et and et <= st:
            raise forms.ValidationError("Время окончания должно быть позже времени начала.")
        return cleaned

    def save(self, commit=True):
        name = self.cleaned_data["name"].strip()
        phone = self.cleaned_data["phone"].strip()

        client = Client.objects.filter(phone=phone).first()
        if not client:
            client = Client.objects.create(name=name, phone=phone)
        else:
            # аккуратно обновим имя, если было пустое/другое
            if name and client.name != name:
                client.name = name
                client.save(update_fields=["name"])

        reservation = super().save(commit=False)
        reservation.client = client
        reservation.status = Reservation.STATUS_BOOKED

        if commit:
            reservation.save()
        return reservation


# Совместимость со старыми импортами (чтобы НЕ ловить ImportError)
ReservationPublicForm = PublicReservationForm


class ReservationForm(forms.ModelForm):
    """Форма для админа/кафе (закрытая часть)."""

    class Meta:
        model = Reservation
        fields = (
            "client",
            "date",
            "start_time",
            "end_time",
            "table_number",
            "guests",
            "status",
        )
        widgets = {
            "client": forms.Select(attrs={"class": "form-select"}),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "start_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "end_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "table_number": forms.NumberInput(attrs={"class": "form-control"}),
            "guests": forms.NumberInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }

    def clean(self):
        cleaned = super().clean()
        st = cleaned.get("start_time")
        et = cleaned.get("end_time")
        if st and et and et <= st:
            raise forms.ValidationError("Время окончания должно быть позже времени начала.")
        return cleaned


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ("name", "phone")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "+7"}),
        }
