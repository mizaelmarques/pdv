import unittest
from decimal import Decimal
from unittest.mock import Mock, MagicMock
from compras.domain import Product
from compras.application.services import OrderService


class TestCarrinhoLogic(unittest.TestCase):
    def setUp(self):
        # Mock dos repositórios para isolar os testes
        self.product_repo = Mock()
        self.order_repo = Mock()
        
        # Produtos dummy para os testes
        self.product1 = Product(
            id=1,
            name="Cimento Portland CPV-ARI",
            description="Cimento de alta resistência",
            price=Decimal("32.90"),
            unit="saco"
        )
        
        self.product2 = Product(
            id=2,
            name="Areia Média",
            description="Areia para concretos",
            price=Decimal("15.50"),
            unit="m³"
        )
        
        # Configuração dos mocks
        self.product_repo.get_by_id.side_effect = lambda pid: {
            1: self.product1,
            2: self.product2
        }.get(pid, None)
        
        # Criação do serviço para testar
        self.service = OrderService(self.product_repo, self.order_repo)

    def test_calcular_total_com_um_produto(self):
        """Testa o cálculo total com um único produto"""
        cart = {1: 1}
        total = self.service._calculate_total(cart)
        self.assertEqual(total, Decimal("32.90"))

    def test_calcular_total_com_varios_produtos(self):
        """Testa o cálculo total com múltiplos produtos"""
        cart = {1: 2, 2: 1}
        total = self.service._calculate_total(cart)
        self.assertEqual(total, Decimal("81.30"))

    def test_calcular_total_com_produto_invalido(self):
        """Testa o cálculo com um produto que não existe"""
        cart = {1: 1, 999: 5}
        total = self.service._calculate_total(cart)
        self.assertEqual(total, Decimal("32.90"))

    def test_calcular_total_quantidade_zero(self):
        """Testa com quantidade zero (não deve contar)"""
        cart = {1: 0, 2: 3}
        total = self.service._calculate_total(cart)
        self.assertEqual(total, Decimal("46.50"))


if __name__ == "__main__":
    unittest.main()
