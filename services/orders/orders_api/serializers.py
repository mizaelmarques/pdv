from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'number', 'total', 'is_finalized', 'created_at']
