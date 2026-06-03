from behave import given, when, then
from decimal import Decimal
from unittest.mock import Mock
from compras.domain import Product
from compras.application.services import OrderService


@given("que existe um produto {name} com id {id:d}, preço R${price} e unidade {unit}")
def step_impl(context, name, id, price, unit):
    if not hasattr(context, "products"):
        context.products = {}
    context.products[id] = Product(
        id=id,
        name=name,
        description=f"Produto {name}",
        price=Decimal(price),
        unit=unit
    )
    
  
    product_repo = Mock()
    order_repo = Mock()
    product_repo.get_by_id.side_effect = lambda pid: context.products.get(pid, None)
    product_repo.get_all.return_value = list(context.products.values())
    
 
    context.order_service = OrderService(product_repo, order_repo)
    context.cart = {}


@given("que o carrinho está vazio")
def step_impl(context):
    context.cart = {}


@when("eu adiciono {qtd:d} unidades do produto de id {id:d} ao carrinho")
def step_impl(context, qtd, id):
    if id in context.cart:
        context.cart[id] += qtd
    else:
        context.cart[id] = qtd


@when("eu adiciono mais {qtd:d} unidades do produto de id {id:d} ao carrinho")
def step_impl(context, qtd, id):
    if id in context.cart:
        context.cart[id] += qtd
    else:
        context.cart[id] = qtd


@when("eu tento adicionar {qtd:d} unidades do produto de id {id:d} ao carrinho")
def step_impl(context, qtd, id):
 
    if id in context.products:
        if id in context.cart:
            context.cart[id] += qtd
        else:
            context.cart[id] = qtd


@then("o carrinho deve ter {count:d} item, que é {name}")
def step_impl(context, count, name):
    # Encontra o produto pelo nome
    product = next((p for p in context.products.values() if p.name == name), None)
    assert product is not None, f"Produto {name} não encontrado"
    
    # Verifica a quantidade de items
    assert len(context.cart) == count, f"Esperado {count} item(s), encontrado {len(context.cart)}"
    assert product.id in context.cart, f"Produto {name} não está no carrinho"


@then("a quantidade do item no carrinho deve ser {qtd:d}")
def step_impl(context, qtd):
    # Verifica a quantidade para o produto único no carrinho
    assert len(context.cart) == 1
    for product_id, cart_qtd in context.cart.items():
        assert cart_qtd == qtd, f"Esperado {qtd}, encontrado {cart_qtd}"


@then("a quantidade total do produto {id:d} no carrinho deve ser {qtd:d}")
def step_impl(context, id, qtd):
    assert id in context.cart
    assert context.cart[id] == qtd, f"Esperado {qtd}, encontrado {context.cart[id]}"


@then("o total da compra deve ser R${total}")
def step_impl(context, total):
    calculated_total = context.order_service._calculate_total(context.cart)
    assert calculated_total == Decimal(total), f"Esperado {total}, encontrado {calculated_total}"


@then("o carrinho deve continuar vazio")
def step_impl(context):
    assert len(context.cart) == 0, "Carrinho não está vazio"


@then("o total da compra deve permanecer R$0.00")
def step_impl(context):
    calculated_total = context.order_service._calculate_total(context.cart)
    assert calculated_total == Decimal("0.00")
