from django.urls import path
from .views import ProductoListCreateView, ProductoUpdateView

urlpatterns = [
    path('', ProductoListCreateView.as_view(), name='listar_crear'),
    path('<int:pk>/', ProductoUpdateView.as_view(), name='actualizar'),
]
