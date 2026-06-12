
# Guia Completo de TDD e BDD do Projeto PDV

---

## 📋 Sumário

1. [Visão Geral do Projeto](#visão-geral)
2. [TDD (Test-Driven Development)](#tdd)
3. [BDD (Behavior-Driven Development)](#bdd)
4. [Como Executar os Testes](#como-executar)
5. [Estrutura de Pastas](#estrutura)

---

## Visão Geral do Projeto <a name="visão-geral"></a>

Projeto de PDV (Ponto de Venda) para loja de materiais de construção, com:
- Arquitetura Limpa (Clean Architecture)
- Princípios SOLID rigorosos
- Design Patterns (Repository, Factory, Observer, Circuit Breaker)
- Microserviços com resiliência
- TDD e BDD completos

---

## TDD (Test-Driven Development) <a name="tdd"></a>

### Estrutura dos Testes

Pasta: `compras/tests/`

Arquivos:
1. `test_payment_processor.py`: Testes unitários para processamento de pagamentos
2. `test_order_service.py`: Testes unitários para a lógica de pedidos
3. `test_carrinho.py`: Testes unitários para a lógica do carrinho
4. `test_integration.py`: Testes de integração (views e fluxo completo)

### Como Executar os Testes Unitários

```bash
# Todos os testes
python manage.py test compras.tests

# Teste específico
python manage.py test compras.tests.test_order_service

# Mais verboso
python manage.py test compras.tests --verbosity=2
```

---

## BDD (Behavior-Driven Development) <a name="bdd"></a>

### Estrutura dos Arquivos Gherkin

Pasta: `features/`

Arquivos:
1. `adicionar_produto_carrinho.feature`: Funcionalidade de adicionar/remover produtos
2. `realizar_compra.feature`: Fluxo básico de compra
3. `fluxo_completo.feature`: Fluxo completo de venda com diferentes formas de pagamento
4. `resiliencia.feature`: Resiliência dos microserviços

Arquivos de Passos:
- `features/steps/adicionar_produto_steps.py`
- `features/steps/pdv_steps.py`

### Sintaxe Gherkin

| Palavra Chave | Uso |
|----------------|-----|
| `Feature`      | Descrição da funcionalidade |
| `Scenario`     | Caso de teste específico |
| `Given`        | Preparação do cenário |
| `When`         | Ações realizadas |
| `Then`         | Resultados esperados |
| `And`          | Continuação da etapa anterior |

### Como Executar os Testes BDD

```bash
# Instalação do Behave (se já não estiver)
pip install behave

# Todos os testes BDD
python -m behave

# Teste de arquivo específico
python -m behave features/fluxo_completo.feature

# Mais verboso
python -m behave --no-color --verbose
```

---

## Como Executar os Testes <a name="como-executar"></a>

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Aplicar Migrações

```bash
python manage.py migrate
```

### 3. Seed dos Produtos

```bash
python manage.py seed_produtos
```

### 4. Rodar Testes TDD

```bash
python manage.py test
```

### 5. Rodar Testes BDD

```bash
python -m behave
```

---

## Estrutura de Pastas <a name="estrutura"></a>

```
projeto-pdv/
├── compras/
│   ├── tests/                          # Testes TDD
│   │   ├── __init__.py
│   │   ├── test_order_service.py
│   │   ├── test_payment_processor.py
│   │   ├── test_carrinho.py
│   │   └── test_integration.py
│   ├── application/                    # Camada de Aplicação
│   ├── domain/                         # Camada de Negócio
│   ├── infrastructure/                 # Camada de Infraestrutura
│   └── templates/
├── features/                           # Testes BDD
│   ├── adicionar_produto_carrinho.feature
│   ├── realizar_compra.feature
│   ├── fluxo_completo.feature
│   ├── resiliencia.feature
│   └── steps/
│       ├── adicionar_produto_steps.py
│       └── pdv_steps.py
├── manage.py
├── requirements.txt
├── README_TDD_BDD.md
└── DOCS_ANALISE_CRITERIOS.md
```

---

## 🔍 Exemplos de Testes

### Exemplo de TDD: `test_order_service.py`
```python
def test_create_order(self):
    cart = {1: 2, 2: 3}
    order = self.service.create_order(cart)
    
    self.assertEqual(order.number, 1)
    self.assertEqual(order.total, Decimal('112.30'))
    self.order_repo.save.assert_called_once()
```

### Exemplo de BDD: `fluxo_completo.feature`
```gherkin
Scenario: Fluxo Normal de Venda (PIX)
    When eu adiciono 3 unidades do produto com id 1 ao carrinho
    And eu adiciono 2 unidades do produto com id 2 ao carrinho
    And eu clico em "Finalizar Venda"
    And na tela de checkout, informo que o pagamento será via "PIX"
    Then o pedido deve ser criado com sucesso
    And o total do pedido deve ser 129.70
    And a forma de pagamento registrada deve ser PIX
```

---
