from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from apps.rooms.models import (Room, RoomType)


class RoomCatalogueListView(ListView):
    model = Room
    template_name = 'rooms/catalogue.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_type'] = RoomType.objects.all()
        return context
