# informe/urls.py
from django.urls import path

from Admin_Bar_FastTrack import views
from .views import listar_informes, exportar_csv

urlpatterns = [
    path('informe_producto/', listar_informes, name='informe_producto'), 
    path('exportar_csv/', exportar_csv, name='exportar_csv'),
]
