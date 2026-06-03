from typing import Optional
from decimal import Decimal
from datetime import datetime
from compras.domain import Order
from compras.domain.repositories import OrderRepository
from compras.models import Pedido


class DjangoOrderRepository(OrderRepository):
    def save(self, order: Order) -> Order:
        pedido, created = Pedido.objects.update_or_create(
            id=order.id if order.id else None,
            defaults={
                'numero': order.number,
                'finalizado': order.is_finalized
            }
        )
        order.id = pedido.id
        order.created_at = pedido.data_criacao
        return order

    def get_next_number(self) -> int:
        last_order = Pedido.objects.order_by('-numero').first()
        return last_order.numero + 1 if last_order else 1

    def get_by_number(self, order_number: int) -> Optional[Order]:
        try:
            pedido = Pedido.objects.get(numero=order_number)
            return Order(
                id=pedido.id,
                number=pedido.numero,
                created_at=pedido.data_criacao,
                total=Decimal('0.00'),
                is_finalized=pedido.finalizado,
                items={}
            )
        except Pedido.DoesNotExist:
            return None
