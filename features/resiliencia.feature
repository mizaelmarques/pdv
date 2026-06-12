
Feature: Resiliência dos Microserviços
  Como usuário do sistema
  Quero que o PDV continue funcionando
  Mesmo quando alguns microserviços estão indisponíveis

  Scenario: Serviço de Produtos está Down
    Given que o serviço de produtos está indisponível
    When eu acesso a página principal do PDV
    Then eu devo ver os produtos de fallback (Cimento e Areia)
    And eu consigo adicionar produtos ao carrinho normalmente

  Scenario: Serviço de Pedidos está Down
    Given que eu tenho o carrinho com 2 sacos de cimento
    And que o serviço de pedidos está indisponível
    When eu clico em "Finalizar Venda"
    Then um pedido temporário deve ser criado
    And eu consigo prosseguir para a tela de checkout

  Scenario: Ambos Serviços estão Down
    Given que o serviço de produtos está indisponível
    And que o serviço de pedidos está indisponível
    When eu navego pelo PDV
    Then o sistema deve continuar funcionando completamente
    And eu consigo realizar uma venda com os dados de fallback
