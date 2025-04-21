from django.urls import path
from . import views

urlpatterns = [
    path('crear/', views.crear_sede, name='crear_sede'),
    path('listar/', views.listar_sedes, name='listar_sedes'),
    path('eliminar/<int:sede_id>/', views.eliminar_sede, name='eliminar_sede'),  
    path('actualizar/<int:sede_id>/', views.editar_sede, name='actualizar_sede'),
]
