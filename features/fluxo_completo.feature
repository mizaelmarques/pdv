
Feature: Fluxo Completo de Venda no PDV
  Como vendedor da loja de materiais de construção
  Quero realizar todas as etapas de uma venda
  Para finalizar pedidos dos clientes

  Background:
    Given que existe os seguintes produtos cadastrados:
      | id | nome                     | preco  | unidade |
      | 1  | Cimento Portland CPV-ARI | 32.90  | saco    |
      | 2  | Areia Média              | 15.50  | m³      |
      | 3  | Brita 1                  | 25.00  | m³      |
    And que o carrinho está vazio

  Scenario: Fluxo Normal de Venda (PIX)
    When eu adiciono 3 unidades do produto com id 1 ao carrinho
    And eu adiciono 2 unidades do produto com id 2 ao carrinho
    And eu clico em "Finalizar Venda"
    And na tela de checkout, informo que o pagamento será via "PIX"
    Then o pedido deve ser criado com sucesso
    And o total do pedido deve ser 129.70
    And a forma de pagamento registrada deve ser PIX

  Scenario: Fluxo Normal de Venda (Cartão de Crédito)
    When eu adiciono 5 unidades do produto com id 3 ao carrinho
    And eu clico em "Finalizar Venda"
    And na tela de checkout, informo que o pagamento será via "cartao"
    Then o pedido deve ser criado com sucesso
    And o total do pedido deve ser 125.00
    And a forma de pagamento registrada deve ser Cartão de Crédito

  Scenario: Remover Item do Carrinho e Finalizar
    When eu adiciono 2 unidades do produto 1 ao carrinho
    And eu adiciono 3 unidades do produto 3 ao carrinho
    And eu removo o produto 1 do carrinho
    And eu clico em "Finalizar Venda"
    Then o total do pedido deve ser 75.00

  Scenario: Limpar Todo o Carrinho
    When eu adiciono 10 unidades do produto 1 ao carrinho
    And eu adiciono 5 unidades do produto 2 ao carrinho
    And eu clico em "Limpar Carrinho"
    Then o carrinho deve estar vazio
