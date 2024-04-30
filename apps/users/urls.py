from django.urls import path
from .views import (AdminPanelView, UserLoginView, UserRegistrationView, EmployeeListView, EmployeeEditView, EmployeeRegistrationView)

app_name = 'users'

urlpatterns = [
    path('signin/', UserRegistrationView.as_view(), name='signin'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('admin-panel/', AdminPanelView.as_view(), name='admin-panel'),
    path('employee/', EmployeeRegistrationView.as_view(), name='employee'),
    path('employee-list/', EmployeeListView.as_view(), name='employee_list'),
    path('employee-edit/<int:rut>', EmployeeEditView.as_view(), name='employee_edit')
]
