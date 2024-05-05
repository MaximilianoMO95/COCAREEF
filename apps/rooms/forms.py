from django import forms
from django.utils.translation import gettext_lazy as _
from .models import (Room, RoomType)

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'capacity', 'description', 'price', 'room_type']
        labels = {
            'name': _('Name'),
            'capacity': _('Capacity'),
            'description': _('Description'),
            'price': _('Price'),
            'room_type': _('Room Type'),
        }


class RoomTypeFilterForm(forms.Form):
    room_type_slug = forms.ModelChoiceField(label=_('Room Type'), queryset=RoomType.objects.all(), required=False)
