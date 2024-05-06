from django.urls import path
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView
from django.contrib.auth.views import LogoutView
from .views import (AdminPanelView, UserLoginView, UserRegistrationView, EmployeeListView, EmployeeEditView, EmployeeRegistrationView)

app_name = 'users'

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('users:login')), name='index'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('signin/', UserRegistrationView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),
    path('admin-panel/', AdminPanelView.as_view(), name='admin-panel'),
    path('employee/', EmployeeRegistrationView.as_view(), name='employee'),
    path('employee-list/', EmployeeListView.as_view(), name='employee_list'),
    path('employee-edit/<int:rut>', EmployeeEditView.as_view(), name='employee_edit')
]
