from django.urls import path
from django.urls import reverse_lazy
from .views import VistaAdminView

from .views import (UserLoginView)

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('vistaadmin/', VistaAdminView.as_view(), name='vista_admin'),

]