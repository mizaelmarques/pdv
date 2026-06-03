import unittest
from decimal import Decimal
from compras.application.services import (
    PaymentProcessorFactory,
    PixPaymentProcessor,
    CardPaymentProcessor
)


class TestPaymentProcessor(unittest.TestCase):
    def test_pix_payment_processor(self):
        processor = PixPaymentProcessor()
        result = processor.process_payment(Decimal('100.50'))
        self.assertIn("PIX", result)
        self.assertIn("100.50", result)

    def test_card_payment_processor(self):
        processor = CardPaymentProcessor()
        result = processor.process_payment(Decimal('250.75'))
        self.assertIn("Cartão de Crédito", result)
        self.assertIn("250.75", result)

    def test_factory_returns_pix_processor(self):
        processor = PaymentProcessorFactory.create_processor("pix")
        self.assertIsInstance(processor, PixPaymentProcessor)

    def test_factory_returns_card_processor(self):
        processor = PaymentProcessorFactory.create_processor("cartao")
        self.assertIsInstance(processor, CardPaymentProcessor)

    def test_factory_raises_error_for_invalid_type(self):
        with self.assertRaises(ValueError):
            PaymentProcessorFactory.create_processor("boleto")


if __name__ == '__main__':
    unittest.main()
