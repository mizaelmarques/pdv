from django.core.management.base import BaseCommand
from products_api.models import Product


class Command(BaseCommand):
    help = 'Popula banco de dados com produtos'

    def handle(self, *args, **options):
        products_data = [
            {'name': 'Cimento Portland CPV-ARI', 'description': 'Cimento de alta resistência para estruturas', 'price': 32.90, 'unit': 'saco'},
            {'name': 'Areia Média', 'description': 'Areia para concretos e argamassas', 'price': 15.50, 'unit': 'm³'},
            {'name': 'Brita 1', 'description': 'Brita para fundações e estruturas', 'price': 85.00, 'unit': 'm³'},
            {'name': 'Brita 0', 'description': 'Brita fina para acabamentos', 'price': 90.00, 'unit': 'm³'},
            {'name': 'Tijolo 8 furos', 'description': 'Tijolo cerâmico para alvenaria', 'price': 0.65, 'unit': 'unidade'},
        ]

        prod_count = Product.objects.count()
        if prod_count == 0:
            for data in products_data:
                Product.objects.create(**data)
            self.stdout.write(self.style.SUCCESS('Produtos criados!'))
        else:
            self.stdout.write(self.style.WARNING('Produtos já existentes!'))
