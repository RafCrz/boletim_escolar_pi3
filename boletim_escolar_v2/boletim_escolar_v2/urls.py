# boletim_escolar_v2/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),           # URL para o painel administrativo
    path('', include('core.urls')),            # Inclui as URLs do app core
]
