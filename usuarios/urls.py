from django.urls import path

from Admin_Bar_FastTrack import views
from . import views


urlpatterns = [
    path('login/', views.vista_login, name='login'),
    path('logout/', views.vista_logout, name='logout'),
    path('registro/', views.vista_registro, name='registro'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/mesero/', views.dashboard_mesero, name='dashboard_mesero'),
    path('dashboard/cajero/', views.dashboard_cajero, name='dashboard_cajero'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
]
    
