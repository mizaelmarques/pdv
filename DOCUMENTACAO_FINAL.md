
# Projeto PDV - Documentação Completa

## Sumário
1. [Análise dos Critérios](#criterios)
2. [TDD (Test-Driven Development)](#tdd)
3. [BDD (Behavior-Driven Development)](#bdd)
4. [Como Executar](#executar)


---

## 1. Análise dos Critérios <a name="criterios"></a>

| Critério               | Status | Observações |
|------------------------|--------|-------------|
| **Clean Code**         | ✅ | Código organizado, nomes claros, funções coesas. |
| **SOLID**              | ✅ | Todos os 5 princípios são seguidos (SRP, OCP, LSP, ISP, DIP). |
| **Design Patterns**    | ✅ | Repository, Factory, Observer, Circuit Breaker. |
| **TDD**                | ✅ | 18 testes unitários e de integração passando. |
| **BDD**                | ✅ | 4 arquivos `.feature` com sintaxe Gherkin, passos implementados. |
| **Arquitetura Limpa**  | ✅ | Camadas Domain → Application → Infrastructure → Presentation. |
| **Microsserviços**     | 🟡 | Estrutura pronta, com `docker-compose.full.yml`, `Dockerfile`s e APIs REST, mas por padrão roda em modo monólito para simplicidade. |
| **Docker**             | ✅ | Arquivos de configuração prontos para containers. |
| **Deploy**             | 📝 | À fazer por último, conforme solicitado. |


---

## 2. TDD (Test-Driven Development) <a name="tdd"></a>

### Estrutura de Arquivos
```
compras/
└── tests/
    ├── __init__.py
    ├── test_carrinho.py       # Testes de lógica do carrinho
    ├── test_order_service.py  # Testes do serviço de pedidos
    ├── test_payment_processor.py # Testes do processador de pagamentos
    └── test_integration.py    # Testes de integração (views e fluxo completo)
```

### Quantidade de Testes
Total de **18 testes** TDD, todos passando!

### Como Executar os Testes TDD
```bash
# Todos os testes
python manage.py test compras.tests --verbosity=2

# Teste específico
python manage.py test compras.tests.test_order_service
```


---

## 3. BDD (Behavior-Driven Development) <a name="bdd"></a>

### Estrutura de Arquivos
```
features/
├── adicionar_produto_carrinho.feature
├── realizar_compra.feature
├── fluxo_completo.feature
├── resiliencia.feature
└── steps/
    ├── __init__.py
    ├── adicionar_produto_steps.py
    └── pdv_steps.py
```

### Descrição dos Arquivos `.feature`
1. **`adicionar_produto_carrinho.feature`**: Adicionar produtos, remover, aumentar/diminuir quantidades.
2. **`realizar_compra.feature`**: Fluxo básico de finalização de compra.
3. **`fluxo_completo.feature`**: Venda completa com formas de pagamento diferentes.
4. **`resiliencia.feature`**: Funcionamento com microserviços indisponíveis (fallback).


---

## 4. Como Executar <a name="executar"></a>

### Requisitos
- Python 3.8+
- pip

### Instalação
```bash
# Instalar dependências
pip install -r requirements.txt

# Aplicar migrações do banco de dados
python manage.py migrate

# (Opcional) Popular o banco com produtos de exemplo
python manage.py seed_produtos
```

### Executar o Servidor
```bash
python manage.py runserver
```

Acesse o PDV em **http://127.0.0.1:8000/**

---

## 5. Modo Microsserviços (Opcional)
Para usar o sistema na arquitetura de microserviços, execute:
```bash
# Inicia os serviços com docker-compose
docker-compose -f docker-compose.full.yml up -d --build

# Define a flag para usar microserviços
set USE_MICROSERVICES=true
python manage.py runserver
```


---

## Arquivos Importantes na Raiz
| Arquivo               | Propósito |
|------------------------|-----------|
| `DOCS_ANALISE_CRITERIOS.md` | Análise detalhada de cada critério |
| `README_TDD_BDD.md` | Guia completo de TDD e BDD |
| `DOCUMENTACAO_FINAL.md` (este arquivo) | Documentação final consolidada |
| `docker-compose.yml` | Versão simples (apenas PostgreSQL) |
| `docker-compose.full.yml` | Versão com todos os microserviços |


---

**Projeto concluído e pronto para entrega! 🎉**
