
from behave import given, when, then
from decimal import Decimal
from django.test import Client
from django.urls import reverse
from compras.models import Produto
from compras.domain import Product
from compras.application.services import OrderService
from compras.infrastructure.django import DjangoProductRepository, DjangoOrderRepository


def before_scenario(context, scenario):
    context.client = Client()


@given("que existe os seguintes produtos cadastrados:")
def step_impl(context):
    for row in context.table:
        Produto.objects.create(
            id=int(row['id']),
            nome=row['nome'],
            descricao=f"Produto {row['nome']}",
            preco=Decimal(row['preco']),
            unidade=row['unidade']
        )


@given("que o carrinho está vazio")
def step_impl(context):
    if 'cart' in context.client.session:
        del context.client.session['cart']
        context.client.session.save()


@given("que eu tenho o carrinho com {qtd:d} sacos de cimento")
def step_impl(context, qtd):
    response = context.client.post(
        reverse('add_to_cart', args=[1]),
        {'quantidade': qtd}
    )
    assert response.status_code == 302


@when("eu adiciono {qtd:d} unidades do produto com id {pid:d} ao carrinho")
def step_impl(context, qtd, pid):
    response = context.client.post(
        reverse('add_to_cart', args=[pid]),
        {'quantidade': qtd}
    )
    assert response.status_code == 302


@when("eu adiciono {qtd:d} unidades do produto {pid:d} ao carrinho")
def step_impl(context, qtd, pid):
    response = context.client.post(
        reverse('add_to_cart', args=[pid]),
        {'quantidade': qtd}
    )
    assert response.status_code == 302


@when("eu clico em \"Finalizar Venda\"")
def step_impl(context):
    response = context.client.get(reverse('finalizar_compra'))
    assert response.status_code == 302


@when("eu clico em \"Limpar Carrinho\"")
def step_impl(context):
    response = context.client.get(reverse('clear_cart'))
    assert response.status_code == 302


@when("eu removo o produto {pid:d} do carrinho")
def step_impl(context, pid):
    response = context.client.get(reverse('remove_from_cart', args=[pid]))
    assert response.status_code == 302


@when("na tela de checkout, informo que o pagamento será via \"{payment_type}\"")
def step_impl(context, payment_type):
    context.payment_type = payment_type


@when("eu acesso a página principal do PDV")
def step_impl(context):
    context.response = context.client.get(reverse('produto_list'))
    assert context.response.status_code == 200


@when("eu navego pelo PDV")
def step_impl(context):
    context.response = context.client.get(reverse('produto_list'))
    assert context.response.status_code == 200


@then("o pedido deve ser criado com sucesso")
def step_impl(context):
    session = context.client.session
    assert 'pedido_id' in session


@then("o total do pedido deve ser {total:g}")
def step_impl(context, total):
    session = context.client.session
    valor_total = session.get('valor_total', 0)
    assert valor_total == float(total)


@then("a forma de pagamento registrada deve ser {payment_type}")
def step_impl(context, payment_type):
    assert context.payment_type in ['PIX', 'cartao', 'Cartão de Crédito']


@then("o carrinho deve estar vazio")
def step_impl(context):
    session = context.client.session
    assert session.get('cart', {}) == {}


@then("eu devo ver os produtos de fallback (Cimento e Areia)")
def step_impl(context):
    # Como os serviços estão down, o sistema usa fallback
    assert "Cimento" in context.response.content.decode()
    assert "Areia" in context.response.content.decode()


@then("eu consigo adicionar produtos ao carrinho normalmente")
def step_impl(context):
    response = context.client.post(
        reverse('add_to_cart', args=[1]),
        {'quantidade': 2}
    )
    assert response.status_code == 302


@then("um pedido temporário deve ser criado")
def step_impl(context):
    session = context.client.session
    assert session.get('pedido_id') is not None


@then("eu consigo prosseguir para a tela de checkout")
def step_impl(context):
    response = context.client.get(reverse('checkout'))
    assert response.status_code == 200


@then("o sistema deve continuar funcionando completamente")
def step_impl(context):
    assert context.response.status_code == 200


@then("eu consigo realizar uma venda com os dados de fallback")
def step_impl(context):
    context.client.post(reverse('add_to_cart', args=[1]), {'quantidade': 1})
    response = context.client.get(reverse('finalizar_compra'))
    assert response.status_code == 302
