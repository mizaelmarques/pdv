Feature: Realizar uma compra
  Como cliente
  Quero adicionar produtos ao carrinho, ver o total e finalizar a compra
  Para receber meus materiais de construção

  Scenario: Adicionar produtos e finalizar compra com PIX
    Given que existe um produto "Cimento Portland" com preço R$32.90
    And que existe um produto "Areia Média" com preço R$15.50
    When eu adiciono 2 unidades do "Cimento Portland"
    And eu adiciono 1 unidade da "Areia Média"
    Then o total da compra deve ser R$81.30
    When eu finalizo a compra com pagamento via PIX
    Then o pedido deve ser criado com sucesso

  Scenario: Cancelar compra limpa o carrinho
    Given que adicionei 1 unidade do produto "Cimento Portland"
    When eu cancelo a compra
    Then o carrinho deve estar vazio
