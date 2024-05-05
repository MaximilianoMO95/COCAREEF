from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Reservation

class OrderCreateForm(forms.Form):
    start_date = forms.DateField(label=_('Start Date'), widget=forms.SelectDateWidget)
    days_of_stay = forms.IntegerField(label=_('Days Of Stay'), min_value=1, max_value=31)


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['start_date', 'days_of_stay', 'room', 'user', 'payment_status', 'deposit_percentage']
        labels = {
            'start_date': _('Start Date'),
            'days_of_stay': _('Days of Stay'),
            'room': _('Room'),
            'user': _('User'),
            'payment_status': _('Payment Status'),
            'deposit_percentage': _('Deposit Percentage'),
        }


class ReservationFilterForm(forms.Form):
    start_date_from = forms.DateField(label=_('From'), required=False, widget=forms.DateInput(attrs={ 'type': 'date' }))
    start_date_to = forms.DateField(label=_('To'), required=False, widget=forms.DateInput(attrs={ 'type': 'date' }))

