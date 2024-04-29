from django.urls import path
from .views import (AdminPanelView, UserLoginView, UserRegistrationView)

app_name = 'users'

urlpatterns = [
    path('signin/', UserRegistrationView.as_view(), name='signin'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('admin-panel/', AdminPanelView.as_view(), name='admin-panel'),
]
