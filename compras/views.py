from django.shortcuts import render, redirect
from decimal import Decimal
from compras.application.services import OrderService
from compras.infrastructure.django import DjangoProductRepository, DjangoOrderRepository
from compras.models import Produto


def _get_order_service() -> OrderService:
    product_repo = DjangoProductRepository()
    order_repo = DjangoOrderRepository()
    return OrderService(product_repo, order_repo)


def produto_list(request):
    service = _get_order_service()
    products = service.get_all_products()
    
    cart = request.session.get('cart', {})
    total = Decimal('0.00')
    
    for product_id_str, quantity in cart.items():
        product = service.get_product_by_id(int(product_id_str))
        if product:
            total += product.price * Decimal(str(quantity))

    # Converte products para o formato que o template espera (compatibilidade)
    produtos_compat = [
        Produto(
            id=p.id,
            nome=p.name,
            descricao=p.description,
            preco=p.price,
            unidade=p.unit
        )
        for p in products
    ]

    return render(request, 'compras/produto_list.html', {
        'produtos': produtos_compat,
        'cart': cart,
        'total': float(total)
    })


def add_to_cart(request, produto_id):
    cart = request.session.get('cart', {})
    produto_id_str = str(produto_id)
    quantidade = int(request.POST.get('quantidade', 1))
    
    cart[produto_id_str] = cart.get(produto_id_str, 0) + quantidade
    request.session['cart'] = cart
    return redirect('produto_list')


def remove_from_cart(request, produto_id):
    cart = request.session.get('cart', {})
    produto_id_str = str(produto_id)
    cart.pop(produto_id_str, None)
    request.session['cart'] = cart
    return redirect('produto_list')


def decrease_quantity(request, produto_id):
    cart = request.session.get('cart', {})
    produto_id_str = str(produto_id)
    
    if produto_id_str in cart:
        if cart[produto_id_str] > 1:
            cart[produto_id_str] -= 1
        else:
            del cart[produto_id_str]
    
    request.session['cart'] = cart
    return redirect('produto_list')


def clear_cart(request):
    request.session['cart'] = {}
    return redirect('produto_list')


def finalizar_compra(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('produto_list')

    service = _get_order_service()
    
    cart_items = {int(k): v for k, v in cart.items()}
    order = service.create_order(cart_items)

    request.session['pedido_id'] = order.number
    request.session['valor_total'] = float(order.total)
    request.session['cart'] = {}

    return redirect('checkout')


def index(request):
    resultado = []
    pedido_id = request.session.get('pedido_id')
    valor = request.session.get('valor_total', 0)

    if request.method == 'POST':
        pedido_id = request.POST.get('pedido_id')
        valor_dec = Decimal(request.POST.get('valor', '0'))
        forma_pagto = request.POST.get('forma_pagto')
        service = _get_order_service()

        try:
            resultado.append(f"--- Iniciando Processamento do Pedido #{pedido_id} ---")
            resultado.append("Conectando ao ambiente de Produção usando a URL: https://api.pagamentos.com/v1")
            
            pagamento_msg = service.finalize_order(
                order_number=int(pedido_id),
                amount=valor_dec,
                payment_type=forma_pagto
            )
            
            resultado.append(pagamento_msg)
            resultado.append("Disparando eventos pós-venda...")
            resultado.append(f"--- Pedido #{pedido_id} Finalizado com Sucesso! ---")
        except Exception as e:
            resultado = [f"Erro: {str(e)}"]

    return render(request, 'compras/index.html', {
        'resultado': resultado,
        'pedido_id': pedido_id,
        'valor': valor
    })
