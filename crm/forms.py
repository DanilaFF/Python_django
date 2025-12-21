from django import forms
from .models import Reservation, Client


class ReservationForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))

    class Meta:
        model = Reservation
        fields = [
            "client",
            "date",
            "start_time",
            "end_time",
            "table_number",
            "guests",
            "status",
        ]


class PublicReservationForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label="Имя")
    phone = forms.CharField(
        max_length=20,
        label="Телефон",
        widget=forms.TextInput(
            attrs={
                "type": "tel",
                "placeholder": "+7XXXXXXXXXX",
            }
        ),
    )

    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))

    class Meta:
        model = Reservation
        fields = [
            "date",
            "start_time",
            "end_time",
            "table_number",
            "guests",
        ]


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ("name", "phone")
