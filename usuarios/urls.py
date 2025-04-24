from django.urls import path

from Admin_Bar_FastTrack import views
from . import views


urlpatterns = [
    path('login/', views.vista_login, name='login'),
    path('logout/', views.vista_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/mesero/', views.dashboard_mesero, name='dashboard_mesero'),
    path('dashboard/cajero/', views.dashboard_cajero, name='dashboard_cajero'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('crear/', views.crear_usuario, name='crear_usuario'),
    path('listar/', views.listar_usuarios, name='listar_usuarios'),
    path('editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),

]
    
