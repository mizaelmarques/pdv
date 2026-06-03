from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
