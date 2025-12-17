from django import forms
from .models import Reservation


class ReservationForm(forms.ModelForm):
    date = forms.DateField(
        input_formats=["%d.%m.%Y"] ,
        widget=forms.DateInput(attrs={"placeholder": "дд.мм.гггг"})
    )

    class Meta:
        model = Reservation
        fields = ["client", "date", "start_time", "end_time", "table_number"]
