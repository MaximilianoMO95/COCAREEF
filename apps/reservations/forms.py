from django import forms

class ReservationForm(forms.Form):
    start_date = forms.DateField(widget=forms.SelectDateWidget)
    days_of_stay = forms.IntegerField(min_value=1, max_value=31)