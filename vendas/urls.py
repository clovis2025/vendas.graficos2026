from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('edit/<int:id>/', views.editar_venda, name='edit'),
    path('delete/<int:id>/', views.deletar_venda, name='delete'),
]