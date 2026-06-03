from abc import ABC, abstractmethod
from decimal import Decimal


class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: Decimal) -> str:
        pass


class PixPaymentProcessor(PaymentProcessor):
    def process_payment(self, amount: Decimal) -> str:
        return f"Pagamento de R${amount:.2f} processado via PIX com sucesso!"


class CardPaymentProcessor(PaymentProcessor):
    def process_payment(self, amount: Decimal) -> str:
        return f"Pagamento de R${amount:.2f} processado via Cartão de Crédito!"


class PaymentProcessorFactory:
    @staticmethod
    def create_processor(payment_type: str) -> PaymentProcessor:
        payment_type_lower = payment_type.lower()
        if payment_type_lower == "pix":
            return PixPaymentProcessor()
        elif payment_type_lower == "cartao":
            return CardPaymentProcessor()
        raise ValueError(f"Tipo de pagamento {payment_type} não suportado!")
