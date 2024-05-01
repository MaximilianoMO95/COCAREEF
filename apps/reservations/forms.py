from django import forms

from .models import Reservation

class OrderCreateForm(forms.Form):
    start_date = forms.DateField(widget=forms.SelectDateWidget)
    days_of_stay = forms.IntegerField(min_value=1, max_value=31)


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['start_date', 'days_of_stay', 'room', 'user', 'is_paid']
