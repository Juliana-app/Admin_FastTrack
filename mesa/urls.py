from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_mesas, name='listar_mesas'),
    path('ocupar/<int:mesa_id>/', views.ocupar_mesa, name='ocupar_mesa'),
    path('liberar/<int:mesa_id>/', views.liberar_mesa, name='liberar_mesa'),
    path('crear/', views.crear_mesa, name='crear_mesa'),
    path('mesas/', views.ver_mesas, name='ver_mesas'),
    path('mesas/editar/<int:mesa_id>/', views.editar_mesa, name='editar_mesa'),
    path('mesas/eliminar/<int:mesa_id>/', views.eliminar_mesa, name='eliminar_mesa'),
]
