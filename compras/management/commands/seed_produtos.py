from django.core.management.base import BaseCommand
from compras.models import Produto


class Command(BaseCommand):
    help = 'Popula o banco de dados com 20 produtos de material de construção'

    def handle(self, *args, **kwargs):
        produtos = [
            {"nome": "Cimento Portland CPV-ARI", "descricao": "Cimento de alta resistência para estruturas", "preco": 32.90, "unidade": "saco"},
            {"nome": "Areia Média", "descricao": "Areia para concretos e argamassas", "preco": 15.50, "unidade": "m³"},
            {"nome": "Brita 1", "descricao": "Brita para fundações e estruturas", "preco": 85.00, "unidade": "m³"},
            {"nome": "Brita 0", "descricao": "Brita fina para acabamentos", "preco": 90.00, "unidade": "m³"},
            {"nome": "Tijolo 8 furos", "descricao": "Tijolo cerâmico para alvenaria", "preco": 0.65, "unidade": "unidade"},
            {"nome": "Bloco de Concreto 14x19x39cm", "descricao": "Bloco estrutural", "preco": 1.80, "unidade": "unidade"},
            {"nome": "Cal Hidratada", "descricao": "Cal para argamassa", "preco": 18.50, "unidade": "saco"},
            {"nome": "Gesso", "descricao": "Gesso para acabamentos", "preco": 25.00, "unidade": "saco"},
            {"nome": "Argamassa Pronta AC-30kg", "descricao": "Argamassa industrializada para assentamento", "preco": 29.90, "unidade": "saco"},
            {"nome": "Massa Corrida 25kg", "descricao": "Massa para nivelamento de paredes", "preco": 45.00, "unidade": "saco"},
            {"nome": "Tinta PVA Branca 18L", "descricao": "Tinta para paredes internas", "preco": 129.90, "unidade": "galão"},
            {"nome": "Verniz Marítimo 3,6L", "descricao": "Verniz para madeira", "preco": 98.00, "unidade": "galão"},
            {"nome": "Madeira Pinus 2x4 (5cm", "descricao": "Madeira para estruturas", "preco": 18.50, "unidade": "m"},
            {"nome": "Madeira Eucalipto 4x4 (10cm)", "descricao": "Madeira para postes", "preco": 35.00, "unidade": "m"},
            {"nome": "Prego 17x27mm", "descricao": "Prego comum", "preco": 9.90, "unidade": "kg"},
            {"nome": "Parafuso Phillips 5x50mm", "descricao": "Parafuso para fixação", "preco": 12.50, "unidade": "kg"},
            {"nome": "Tubo PVC 100mm (4\")", "descricao": "Tubo para esgoto", "preco": 42.00, "unidade": "m"},
            {"nome": "Tubo PVC 50mm (2\")", "descricao": "Tubo para água fria", "preco": 18.50, "unidade": "m"},
            {"nome": "Telha de Fibrocimento 2,44x1,10m", "descricao": "Telha para cobertura", "preco": 55.00, "unidade": "unidade"},
            {"nome": "Fio Elétrico 2,5mm² (100m)", "descricao": "Fio para instalações elétricas", "preco": 89.00, "unidade": "rolo"},
        ]

        for produto_data in produtos:
            Produto.objects.create(**produto_data)
            self.stdout.write(self.style.SUCCESS(f"Produto '{produto_data['nome']} criado com sucesso!"))
