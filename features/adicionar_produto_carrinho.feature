Feature: Adicionar Produto ao Carrinho
  Como cliente da loja de materiais de construção
  Quero adicionar produtos ao carrinho, informando a quantidade
  Para ver o total da compra atualizado em tempo real

  Background:
    Dado que existe um produto "Cimento Portland CPV-ARI" com id 1, preço R$32.90 e unidade "saco"
    E que existe um produto "Areia Média" com id 2, preço R$15.50 e unidade "m³"
    E que o carrinho está vazio

  Scenario: Adicionar um produto com quantidade 1 (caminho feliz)
    Quando eu adiciono 1 unidade do produto de id 1 ao carrinho
    Então o carrinho deve ter 1 item, que é "Cimento Portland CPV-ARI"
    E o total da compra deve ser R$32.90

  Scenario: Adicionar um produto com quantidade maior que 1
    Quando eu adiciono 3 unidades do produto de id 1 ao carrinho
    Então o carrinho deve ter 1 item, que é "Cimento Portland CPV-ARI"
    E a quantidade do item no carrinho deve ser 3
    E o total da compra deve ser R$98.70

  Scenario: Adicionar o mesmo produto duas vezes (acumula quantidade)
    Quando eu adiciono 2 unidades do produto de id 1 ao carrinho
    E eu adiciono mais 2 unidades do produto de id 1 ao carrinho
    Então a quantidade total do produto 1 no carrinho deve ser 4
    E o total da compra deve ser R$131.60

  Scenario: Adicionar múltiplos produtos diferentes
    Quando eu adiciono 2 unidades do produto de id 1 ao carrinho
    E eu adiciono 1 unidade do produto de id 2 ao carrinho
    Então o carrinho deve ter 2 itens
    E o total da compra deve ser R$81.30

  Scenario: Tentar adicionar produto com id inválido (cenário de erro)
    Quando eu tento adicionar 1 unidade do produto de id 999 ao carrinho
    Então o carrinho deve continuar vazio
    E o total da compra deve permanecer R$0.00
