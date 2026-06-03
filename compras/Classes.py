class ConfigSistema:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(ConfigSistema, cls).__new__(cls)
            cls._instancia.api_pagamento = "https://api.pagamentos.com/v1"
            cls._instancia.modo_ambiente = "Produção"
        return cls._instancia

class MetodoPagamento:
    def processar(self, valor):
        raise NotImplementedError("O método processar deve ser implementado.")

class PagamentoPix(MetodoPagamento):
    def processar(self, valor):
        return f"Pagamento de R$ {valor:.2f} processado via PIX com sucesso!"

class PagamentoCartao(MetodoPagamento):
    def processar(self, valor):
        return f"Pagamento de R$ {valor:.2f} processado via Cartão de Crédito!"

class FabricaPagamento:
    @staticmethod
    def criar_forma_pagamento(tipo):
        if tipo.lower() == "pix":
            return PagamentoPix()
        elif tipo.lower() == "cartao":
            return PagamentoCartao()
        else:
            raise ValueError("Forma de pagamento não suportada.")

class Observer:
    def atualizar(self, pedido_id):
        raise NotImplementedError

class SistemaEstoque(Observer):
    def atualizar(self, pedido_id):
        print(f"[ESTOQUE]: Pedido {pedido_id} aprovado! Separando produtos no armazém.")

class SistemaNotificacao(Observer):
    def atualizar(self, pedido_id):
        print(f"[NOTIFICAÇÃO]: Enviando e-mail/WhatsApp para o cliente: Seu pedido {pedido_id} foi confirmado!")

class FachadaCompra:
    def __init__(self):
        self.config = ConfigSistema()
        
        self.sistema_estoque = SistemaEstoque()
        self.sistema_notificacao = SistemaNotificacao()
        
        self.observadores = [self.sistema_estoque, self.sistema_notificacao]

    def finalizar_pedido(self, pedido_id, valor, forma_pagto):
        print(f"\n--- Iniciando Processamento do Pedido #{pedido_id} ---")
        print(f"Conectando ao ambiente de {self.config.modo_ambiente} usando a URL: {self.config.api_pagamento}")
        
        processador = FabricaPagamento.criar_forma_pagamento(forma_pagto)
        resultado_pagto = processador.processar(valor)
        print(resultado_pagto)
        
        print("Disparando eventos pós-venda...")
        for observador in self.observadores:
            observador.atualizar(pedido_id)
            
        print(f"--- Pedido #{pedido_id} Finalizado com Sucesso! ---\n")