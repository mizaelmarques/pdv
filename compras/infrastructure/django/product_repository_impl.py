from typing import List, Optional
from compras.domain import Product
from compras.domain.repositories import ProductRepository
from compras.models import Produto


class DjangoProductRepository(ProductRepository):
    def get_all(self) -> List[Product]:
        produtos = Produto.objects.all()
        return [
            Product(
                id=produto.id,
                name=produto.nome,
                description=produto.descricao,
                price=produto.preco,
                unit=produto.unidade
            )
            for produto in produtos
        ]

    def get_by_id(self, product_id: int) -> Optional[Product]:
        try:
            produto = Produto.objects.get(id=product_id)
            return Product(
                id=produto.id,
                name=produto.nome,
                description=produto.descricao,
                price=produto.preco,
                unit=produto.unidade
            )
        except Produto.DoesNotExist:
            return None
