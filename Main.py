from Classes import FachadaCompra

if __name__ == "__main__":
    ecommerce = FachadaCompra()

    ecommerce.finalizar_pedido(pedido_id=1001, valor=250.50, forma_pagto="pix")
    
    ecommerce.finalizar_pedido(pedido_id=1002, valor=1200.00, forma_pagto="cartao")