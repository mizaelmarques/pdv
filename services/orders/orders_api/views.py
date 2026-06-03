from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from decimal import Decimal


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=['post'])
    def create_order(self, request):
        last_order = Order.objects.order_by('-number').first()
        new_number = last_order.number + 1 if last_order else 1
        total = Decimal(request.data.get('total', '0.00'))
        order = Order.objects.create(number=new_number, total=total, is_finalized=True)
        serializer = self.get_serializer(order)
        return Response(serializer.data)
