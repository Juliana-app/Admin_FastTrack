from django.urls import path
from .views import (
    vista_login, vista_logout, vista_registro, dashboard,
    dashboard_mesero, dashboard_cajero, dashboard_admin
)

urlpatterns = [
    path('login/', vista_login, name='login'),
    path('logout/', vista_logout, name='logout'),
    path('registro/', vista_registro, name='registro'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/mesero/', dashboard_mesero, name='dashboard_mesero'),
    path('dashboard/cajero/', dashboard_cajero, name='dashboard_cajero'),
    path('dashboard/admin/', dashboard_admin, name='dashboard_admin'),
]
