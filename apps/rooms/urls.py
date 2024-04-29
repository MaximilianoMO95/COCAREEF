from django.urls import path
from .views import (RoomCatalogueListView, RoomCreateView, RoomUpdateView)

app_name = 'rooms'

urlpatterns = [
    path('', RoomCatalogueListView.as_view(), name='catalogue'),
    path('edit/<int:room_id>', RoomUpdateView.as_view(), name='edit'),
    path('create/', RoomCreateView.as_view(), name='create'),
]
