from django.urls import path
from . import views

urlpatterns = [
    path('', views.produto_list, name='produto_list'),
    path('add/<int:produto_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:produto_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('decrease/<int:produto_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('clear/', views.clear_cart, name='clear_cart'),
    path('finalizar/', views.finalizar_compra, name='finalizar_compra'),
    path('checkout/', views.index, name='checkout'),
]
