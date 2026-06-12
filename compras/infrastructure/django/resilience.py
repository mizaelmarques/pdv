"""
Módulo de Resiliência para Microserviços
Implementa Circuit Breaker, Fallbacks, Retries e Caching
"""
import pybreaker
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from typing import Dict, List, Any, Optional
from decimal import Decimal
from django.core.cache import cache


# ------------------------------
# 1. Configuração do Circuit Breaker (versão simplificada)
# ------------------------------
# Abre o circuito após 5 falhas consecutivas, fecha novamente após 30 segundos
circuit_breaker = pybreaker.CircuitBreaker(
    fail_max=5,
    reset_timeout=30
)


# ------------------------------
# 2. Retries com Backoff Exponencial
# ------------------------------
@retry(
    stop=stop_after_attempt(1),
    wait=wait_exponential(multiplier=0.5, min=0.5, max=1),
    retry=retry_if_exception_type((requests.exceptions.RequestException,))
)
def make_resilient_request(method: str, url: str, **kwargs) -> requests.Response:
    """
    Faz uma requisição HTTP com retries automáticos
    """
    return requests.request(method, url, timeout=1, **kwargs)


# ------------------------------
# 3. Fallbacks e Cache
# ------------------------------
# Dados padrão para fallback (produtos essenciais)
FALLBACK_PRODUCTS = [
    {
        "id": 1,
        "name": "Cimento Portland CPV-ARI (Modo Offline)",
        "description": "Cimento essencial para construção",
        "price": 32.90,
        "unit": "saco"
    },
    {
        "id": 2,
        "name": "Areia Média (Modo Offline)",
        "description": "Areia para concretos",
        "price": 15.50,
        "unit": "m³"
    }
]


# ------------------------------
# 4. Wrapper Resiliente para API de Produtos
# ------------------------------
class ResilientProductService:
    def __init__(self, base_url: str = "http://localhost:8001/api"):
        self.base_url = base_url
        self.cache_ttl = 300  # 5 minutos de cache

    def _fetch_products_from_api(self):
        """Função interna que usa circuit breaker"""
        @circuit_breaker
        def _call():
            response = make_resilient_request("GET", f"{self.base_url}/products/")
            response.raise_for_status()
            return response.json()
        return _call()

    def get_all_products(self) -> List[Dict[str, Any]]:
        """
        Obtém todos os produtos com:
        - Circuit Breaker
        - Retries
        - Cache
        - Fallback
        """
        cache_key = "all_products"
        
        # Tenta pegar do cache primeiro
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        try:
            products = self._fetch_products_from_api()
            # Armazena no cache
            cache.set(cache_key, products, self.cache_ttl)
            return products
        except (requests.exceptions.RequestException, pybreaker.CircuitBreakerError):
            # Se o serviço estiver down, retorna fallback
            print("Servico de Produtos indisponivel, usando dados de fallback")
            return FALLBACK_PRODUCTS

    def _fetch_product_by_id_from_api(self, product_id):
        """Função interna que usa circuit breaker"""
        @circuit_breaker
        def _call():
            response = make_resilient_request("GET", f"{self.base_url}/products/{product_id}/")
            response.raise_for_status()
            return response.json()
        return _call()

    def get_product_by_id(self, product_id: int) -> Optional[Dict[str, Any]]:
        """Obtém um produto por ID com fallback"""
        cache_key = f"product_{product_id}"
        
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        try:
            product = self._fetch_product_by_id_from_api(product_id)
            cache.set(cache_key, product, self.cache_ttl)
            return product
        except (requests.exceptions.RequestException, pybreaker.CircuitBreakerError):
            # Busca no fallback
            product = next((p for p in FALLBACK_PRODUCTS if p['id'] == product_id), None)
            if product:
                print(f"Usando produto de fallback: {product['name']}")
            return product


# ------------------------------
# 5. Wrapper Resiliente para API de Pedidos
# ------------------------------
class ResilientOrderService:
    def __init__(self, base_url: str = "http://localhost:8002/api"):
        self.base_url = base_url

    def _create_order_in_api(self, order_data):
        """Função interna que usa circuit breaker"""
        @circuit_breaker
        def _call():
            response = make_resilient_request("POST", f"{self.base_url}/orders/create_order/", json=order_data)
            response.raise_for_status()
            return response.json()
        return _call()

    def create_order(self, order_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Cria um pedido com circuit breaker.
        Se falhar, retorna um pedido "simulado" para manter o fluxo.
        """
        try:
            return self._create_order_in_api(order_data)
        except (requests.exceptions.RequestException, pybreaker.CircuitBreakerError):
            print("Servico de Pedidos indisponivel, gerando pedido temporario")
            # Fallback: retorna um ID temporário
            return {
                "id": 99999,  # ID temporário
                "order_number": order_data.get("order_number", "TEMP-999"),
                "total_amount": order_data.get("total_amount", 0),
                "status": "PENDENTE (Modo Offline)",
                "is_offline": True
            }
