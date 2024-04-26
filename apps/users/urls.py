from django.urls import path
from django.urls import reverse_lazy


from .views import (UserLoginView)

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),

]