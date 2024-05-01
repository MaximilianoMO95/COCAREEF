from django import forms
from .models import (Room, RoomType)

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'capacity', 'description', 'price', 'room_type']


class RoomTypeFilterForm(forms.Form):
    room_type_slug = forms.ModelChoiceField(label='Tipo De Habitacion',queryset=RoomType.objects.all(), empty_label='All', required=False)
