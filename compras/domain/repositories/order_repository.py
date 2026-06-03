from abc import ABC, abstractmethod
from typing import Optional
from compras.domain import Order


class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> Order:
        pass

    @abstractmethod
    def get_next_number(self) -> int:
        pass

    @abstractmethod
    def get_by_number(self, order_number: int) -> Optional[Order]:
        pass
