from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_mesas, name='listar_mesas'),
    path('ocupar_mesa/<int:mesa_id>/', views.ocupar_mesa, name='ocupar_mesa'),
    path('liberar_mesa/<int:mesa_id>/', views.liberar_mesa, name='liberar_mesa'),
    path('crear_mesa/', views.crear_mesa, name='crear_mesa'),
    path('editar_mesa/<int:mesa_id>/', views.editar_mesa, name='editar_mesa'),
    path('eliminar_mesa/<int:mesa_id>/', views.eliminar_mesa, name='eliminar_mesa'),
    path('ver_mesas/', views.ver_mesas, name='ver_mesas'),
]
