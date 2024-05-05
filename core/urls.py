"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
from django.urls import path, include

urlpatterns = [
    path('set-language/', set_language, name='set_language'),
    path('admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
    path('', include('apps.users.urls', namespace='users')),
    path('rooms/', include('apps.rooms.urls', namespace='rooms')),
    path('reservations/', include('apps.reservations.urls', namespace='reservations')),
)
