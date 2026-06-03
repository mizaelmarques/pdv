import unittest
from decimal import Decimal
from unittest.mock import Mock
from datetime import datetime
from compras.domain import Product, Order
from compras.application.services import OrderService


class TestOrderService(unittest.TestCase):
    def setUp(self):
        self.product_repo = Mock()
        self.order_repo = Mock()
        
        self.product_repo.get_all.return_value = [
            Product(id=1, name="Cimento", description="Cimento Portland", price=Decimal('32.90'), unit="saco"),
            Product(id=2, name="Areia", description="Areia média", price=Decimal('15.50'), unit="m³"),
        ]
        
        self.product_repo.get_by_id.side_effect = lambda pid: next(
            (p for p in self.product_repo.get_all() if p.id == pid), None
        )
        
        self.order_repo.get_next_number.return_value = 1
        
        def save_order(order):
            order.id = 1
            order.created_at = datetime.now()
            return order
        
        self.order_repo.save.side_effect = save_order
        
        self.service = OrderService(self.product_repo, self.order_repo)

    def test_create_order(self):
        cart = {1: 2, 2: 3}
        order = self.service.create_order(cart)
        
        self.assertEqual(order.number, 1)
        self.assertEqual(order.total, Decimal('112.30'))
        self.order_repo.save.assert_called_once()

    def test_calculate_total(self):
        cart = {1: 2}  # 2 sacos de cimento
        order = self.service.create_order(cart)
        
        self.assertEqual(order.total, Decimal('65.80'))

    def test_finalize_order(self):
        result = self.service.finalize_order(
            order_number=1,
            amount=Decimal('100.00'),
            payment_type="pix"
        )
        
        self.assertIn("PIX", result)
        self.assertIn("100.00", result)


if __name__ == '__main__':
    unittest.main()
