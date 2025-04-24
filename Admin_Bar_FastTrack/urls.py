from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from Admin_Bar_FastTrack import views 
from django.conf import settings
from django.conf.urls.static import static
from usuarios.views import redireccion_por_rol

urlpatterns = [
    path('', redireccion_por_rol, name='inicio'),
    
    path('admin/', admin.site.urls),
    path('api/usuarios/', include('usuarios.urls')),
    path('api/inventario/', include('inventario.urls')),
    path('api/pedidos/', include('pedidos.urls')),  
    path('productos/', include('productos.urls')),
    path('api/sede/', include('sede.urls')),
    path('precios/', include('historial.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

