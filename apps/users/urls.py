from django.urls import path
from .views import (UserRegistrationView)

app_name = 'users'

urlpatterns = [
    path('signin/', UserRegistrationView.as_view(), name='signin'),
]
