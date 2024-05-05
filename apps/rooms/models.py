from django.db import models
from django.utils.translation import gettext_lazy as _

class RoomType(models.Model):
    name = models.CharField(_('name'), max_length=50)

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(_('name'), max_length=100)
    capacity = models.IntegerField(_('capacity'))
    description = models.TextField(_('description'))
    price = models.PositiveIntegerField(_('price'))
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, verbose_name=_('room_type'))

    def __str__(self):
        return self.name
