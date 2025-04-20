from django.urls import path
from .views import ProductoListCreateView, ProductoUpdateView, dashboard_general

urlpatterns = [
    path('', ProductoListCreateView.as_view(), name='listar_crear'),
    path('<int:pk>/', ProductoUpdateView.as_view(), name='actualizar'),
    path('panel/', dashboard_general, name='dashboard_general'),

]
