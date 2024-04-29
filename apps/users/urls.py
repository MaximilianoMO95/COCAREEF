from django.urls import path, include
from django.urls import reverse_lazy

from .views import UserLoginView, EmployeeListView,EmployeeEditView, EmployeeRegistrationView, VistaAdminView

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('vistaadmin/', VistaAdminView.as_view(), name='vista_admin'),
    path('employee/', EmployeeRegistrationView.as_view(), name='employee'),
    path('employee-list/', EmployeeListView.as_view(), name='employee_list'),
    path('employee_edit/<int:rut>', EmployeeEditView.as_view(), name='employee_edit')

]