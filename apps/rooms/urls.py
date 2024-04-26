from django.urls import path

from apps.rooms.views import RoomCatalogueListView

app_name = 'rooms'

urlpatterns = [
    path('', RoomCatalogueListView.as_view(), name='catalogue'),
]
