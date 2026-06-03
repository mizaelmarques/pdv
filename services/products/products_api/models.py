from django.db import models
from decimal import Decimal


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    unit = models.CharField(max_length=50, default='unidade')

    def __str__(self):
        return f'{self.name} - R${self.price:.2f}/{self.unit}'
