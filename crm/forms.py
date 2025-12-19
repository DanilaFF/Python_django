from django import forms
from .models import Reservation



class ReservationForm(forms.ModelForm):
    date = forms.DateField(
        input_formats=["%d.%m.%Y"],
        widget=forms.DateInput(attrs={"placeholder": "дд.мм.гггг"})
    )

    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={"type": "time"})
    )
    end_time = forms.TimeField(
        widget=forms.TimeInput(attrs={"type": "time"})
    )

    class Meta:
        model = Reservation
        fields = ["client", "date", "start_time", "end_time", "table_number", "guests"]

from .models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ("name", "phone")
        labels = {
            "name": "Имя",
            "phone": "Телефон",
        }

