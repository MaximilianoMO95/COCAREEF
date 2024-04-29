from django.views.generic import ListView

from apps.rooms.models import (Room, RoomType)

class RoomCatalogueListView(ListView):
    model = Room
    template_name = 'rooms/catalogue.html'

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
