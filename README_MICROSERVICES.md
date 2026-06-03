# Microserviços do Projeto

## Estrutura
- **services/products/**: Microserviço de Produtos (API REST)
- **services/orders/**: Microserviço de Pedidos (API REST)
- **./**: Gateway/Frontend (monólito original)

## Como Executar com Docker

1. Instale Docker e Docker Compose
2. Inicie os serviços:
```bash
docker-compose -f docker-compose.full.yml up --build
```

3. Acesse as APIs e o frontend:
- **API Produtos**: http://localhost:8001/api/products/
- **API Pedidos**: http://localhost:8002/api/orders/
- **Frontend/Gateway**: http://localhost:8000/

## Para Configurar os Bancos de Dados
As migrações serão executadas automaticamente, mas para seed dos produtos:
```bash
# No container do products-service
docker exec -it products-service python manage.py makemigrations
docker exec -it products-service python manage.py migrate
docker exec -it products-service python manage.py seed
```

Para os pedidos:
```bash
docker exec -it orders-service python manage.py makemigrations
docker exec -it orders-service python manage.py migrate
```
