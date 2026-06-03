from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from orders_api.views import OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
