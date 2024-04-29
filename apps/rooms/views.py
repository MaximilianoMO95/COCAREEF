from django.views import View
from django.views.generic import ListView
from django.shortcuts import (render, get_object_or_404, redirect)

from apps.rooms.models import (Room, RoomType)
from .forms import RoomForm

class RoomCatalogueListView(ListView):
    model = Room
    template_name = 'rooms/catalogue.html'

    def get_template_names(self):
        if self.request.user.is_superuser:
            return ['rooms/admin/catalogue.html']

        return self.template_name


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_types'] = RoomType.objects.all()
        return context


    def get_queryset(self):
        queryset = super().get_queryset()
        room_type_slug = self.request.GET.get('room_type_slug')

        if room_type_slug:
            query_subset = queryset.filter(room_type__name=room_type_slug)
            if query_subset.exists():
                return query_subset

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
            return redirect('rooms:catalogue', room_id=room.id)

        return render(request, self.template_name, { 'form': form, 'room': room })


def delete_room(request, room_id):
    room = Room.objects.get(id=room_id)
    room.delete()

    return redirect('rooms:catalogue')
