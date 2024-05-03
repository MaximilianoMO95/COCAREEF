from django.urls import path
from .views import (RoomCatalogueListView, RoomCreateView, RoomDetailsView, RoomUpdateView, delete_room)

app_name = 'rooms'

urlpatterns = [
    path('', RoomCatalogueListView.as_view(), name='catalogue'),
    path('edit/<int:room_id>', RoomUpdateView.as_view(), name='edit'),
    path('delete/<int:room_id>', delete_room, name='delete'),
    path('create/', RoomCreateView.as_view(), name='create'),
    path('details/<int:room_id>', RoomDetailsView.as_view(), name='details'),
]
