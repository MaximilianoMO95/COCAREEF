from django.contrib import admin

from apps.rooms.models import (Room, RoomType)

admin.site.register(RoomType)
admin.site.register(Room)
