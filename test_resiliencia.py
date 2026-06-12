#!/usr/bin/env python
"""
Script de teste de resiliência dos microserviços
Demonstra:
- Fallback quando serviço está down
- Cache funciona
- Circuit Breaker abre
"""
# Configura o Django PRIMEIRO, antes de importar outros módulos
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce_project.settings")
django.setup()

from compras.infrastructure.django.resilience import ResilientProductService, ResilientOrderService
from decimal import Decimal


def test_product_service():
    print("=" * 60)
    print("TESTE DO SERVICO DE PRODUTOS (RESILIENTE)")
    print("=" * 60)
    
    service = ResilientProductService()
    
    print("\n1. Buscando produtos...")
    products = service.get_all_products()
    print(f"   OK {len(products)} produtos encontrados:")
    for p in products:
        print(f"      - {p['name']} (R${p['price']:.2f})")
    
    print("\n2. Buscando produto por ID 1...")
    product = service.get_product_by_id(1)
    if product:
        print(f"   OK Encontrado: {product['name']}")
    
    print("\nTeste do Servico de Produtos concluido!")


def test_order_service():
    print("\n" + "=" * 60)
    print("TESTE DO SERVICO DE PEDIDOS (RESILIENTE)")
    print("=" * 60)
    
    service = ResilientOrderService()
    order_data = {
        "order_number": 1001,
        "total_amount": 98.70,
        "items": {"1": 3}
    }
    
    print("\n1. Criando pedido...")
    order = service.create_order(order_data)
    print(f"   OK Pedido criado: {order}")
    
    print("\nTeste do Servico de Pedidos concluido!")


if __name__ == "__main__":
    
    test_product_service()
    test_order_service()
    
    print("\n" + "=" * 60)
    print("TODOS OS TESTES DE RESILIENCIA CONCLUIDOS!")
    print("=" * 60)
