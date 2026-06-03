from decimal import Decimal
from datetime import datetime
from typing import List, Dict, Optional
from compras.domain import Product, Order
from compras.domain.repositories import ProductRepository, OrderRepository
from .payment_processor import PaymentProcessorFactory, PaymentProcessor
from .observers import OrderObserver, InventorySystem, NotificationSystem


class OrderService:
    def __init__(
        self,
        product_repository: ProductRepository,
        order_repository: OrderRepository
    ):
        self.product_repository = product_repository
        self.order_repository = order_repository
        self.observers: List[OrderObserver] = [InventorySystem(), NotificationSystem()]

    def create_order(self, cart_items: Dict[int, int]) -> Order:
        total = self._calculate_total(cart_items)
        order_number = self.order_repository.get_next_number()

        order = Order(
            id=None,
            number=order_number,
            created_at=datetime.now(),
            total=total,
            is_finalized=False,
            items=cart_items
        )

        return self.order_repository.save(order)

    def finalize_order(
        self,
        order_number: int,
        amount: Decimal,
        payment_type: str
    ) -> str:
        processor = PaymentProcessorFactory.create_processor(payment_type)
        result = processor.process_payment(amount)

        for observer in self.observers:
            observer.update(order_number)

        return result

    def _calculate_total(self, cart_items: Dict[int, int]) -> Decimal:
        total = Decimal('0.00')
        for product_id, quantity in cart_items.items():
            if self._is_valid_quantity(quantity):
                total += self._calculate_product_subtotal(product_id, quantity)
        return round(total, 2)
        
    def _is_valid_quantity(self, quantity: int) -> bool:
        """Valida se a quantidade é positiva (maior que zero)"""
        return quantity > 0
        
    def _calculate_product_subtotal(self, product_id: int, quantity: int) -> Decimal:
        """Calcula o subtotal para um produto individual"""
        product = self.product_repository.get_by_id(product_id)
        if not product:
            return Decimal('0.00')
        return product.price * Decimal(str(quantity))

    def get_all_products(self) -> List[Product]:
        return self.product_repository.get_all()

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        return self.product_repository.get_by_id(product_id)
