from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from Admin_Bar_FastTrack import views 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/usuarios/', include('usuarios.urls')),
    path('api/inventario/', include('inventario.urls')),
    path('api/pedidos/', include('pedidos.urls')),  
    path('', lambda request: redirect('/api/pedidos/mesero/')),
]
