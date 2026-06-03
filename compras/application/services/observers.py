from abc import ABC, abstractmethod


class OrderObserver(ABC):
    @abstractmethod
    def update(self, order_number: int):
        pass


class InventorySystem(OrderObserver):
    def update(self, order_number: int):
        print(f"[ESTOQUE] Pedido {order_number} aprovado! Separando produtos no armazém.")


class NotificationSystem(OrderObserver):
    def update(self, order_number: int):
        print(f"[NOTIFICAÇÃO] Enviando email/WhatsApp para o cliente: Pedido {order_number} confirmado!")
