from django.db import models
from decimal import Decimal


class Order(models.Model):
    number = models.IntegerField(unique=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    is_finalized = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pedido #{self.number} - R${self.total:.2f}'
