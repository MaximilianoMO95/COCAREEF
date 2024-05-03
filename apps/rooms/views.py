from django.views import View
from django.views.generic import ListView
from django.shortcuts import (render, get_object_or_404, redirect)

from apps.rooms.models import Room
from .forms import (RoomForm, RoomTypeFilterForm)

class RoomCatalogueListView(ListView):
    model = Room
    template_name = 'rooms/catalogue.html'
    filter_form = RoomTypeFilterForm

    def get_template_names(self):
        if self.request.user.is_superuser:
            return ['rooms/admin/catalogue.html']
        return self.template_name


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filter_form(self.request.GET)
        return context


    def get_queryset(self):
        queryset = super().get_queryset()
        form = self.filter_form(self.request.GET)

        if form.is_valid():
            room_type_slug = form.cleaned_data.get('room_type_slug')
            if room_type_slug:
                queryset = queryset.filter(room_type__name=room_type_slug)

        return queryset


class RoomCreateView(View):
    template_name = 'rooms/admin/create.html'

    def get(self, request):
        form = RoomForm()
        return render(request, self.template_name, { 'form': form })


    def post(self, request):
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rooms:catalogue')

        return render(request, self.template_name, { 'form': form })


class RoomUpdateView(View):
    template_name = 'rooms/admin/update.html'

    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        form = RoomForm(instance=room)
        return render(request, self.template_name, { 'form': form, 'room': room })


    def post(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('rooms:catalogue')

        return render(request, self.template_name, { 'form': form, 'room': room })


def delete_room(request, room_id):
    room = Room.objects.get(id=room_id)
    room.delete()

    return redirect('rooms:catalogue')


class RoomDetailsView(View):
    template_name = 'rooms/details.html'

    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        return render(request, self.template_name, { 'room': room })
