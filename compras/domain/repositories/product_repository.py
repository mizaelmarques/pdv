from abc import ABC, abstractmethod
from typing import List, Optional
from compras.domain import Product


class ProductRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Product]:
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        pass
