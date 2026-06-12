
from django.test import TestCase, Client
from decimal import Decimal
from django.urls import reverse
from compras.models import Produto
from compras.application.services import OrderService
from compras.infrastructure.django import DjangoProductRepository, DjangoOrderRepository


class TestPDVIntegration(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Limpa produtos existentes
        Produto.objects.all().delete()
        
        # Cria produtos de teste
        self.produto_cimento = Produto.objects.create(
            nome="Cimento Portland CPV-ARI",
            descricao="Cimento de alta resistência para construções",
            preco=Decimal('32.90'),
            unidade="saco"
        )
        self.produto_areia = Produto.objects.create(
            nome="Areia Média",
            descricao="Areia para concretos e argamassas",
            preco=Decimal('15.50'),
            unidade="m³"
        )
        
        self.product_repo = DjangoProductRepository()
        self.order_repo = DjangoOrderRepository()
        self.service = OrderService(self.product_repo, self.order_repo)

    def test_listar_produtos_view(self):
        """Testa se a página principal lista os produtos corretamente"""
        response = self.client.get(reverse('produto_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cimento Portland CPV-ARI")
        self.assertContains(response, "Areia Média")

    def test_adicionar_produto_carrinho(self):
        """Testa a funcionalidade de adicionar produto ao carrinho via view"""
        # Adiciona produto com quantidade 2
        response = self.client.post(
            reverse('add_to_cart', args=[self.produto_cimento.id]),
            {'quantidade': 2}
        )
        self.assertRedirects(response, reverse('produto_list'))
        
        # Verifica se o carrinho na sessão está correto
        session = self.client.session
        self.assertEqual(session['cart'], {str(self.produto_cimento.id): 2})

    def test_calculo_total_carrinho(self):
        """Testa se o total é calculado corretamente na view"""
        # Adiciona 2 sacos de cimento e 1 m³ de areia
        self.client.post(
            reverse('add_to_cart', args=[self.produto_cimento.id]),
            {'quantidade': 2}
        )
        self.client.post(
            reverse('add_to_cart', args=[self.produto_areia.id]),
            {'quantidade': 1}
        )
        
        response = self.client.get(reverse('produto_list'))
        self.assertEqual(response.status_code, 200)
        # Total: (32.90 *2) + (15.50 *1) = 65.80 +15.50=81.30
        self.assertContains(response, "81.30")

    def test_remover_produto_carrinho(self):
        """Testa a funcionalidade de remover produto do carrinho"""
        # Adiciona produto
        self.client.post(
            reverse('add_to_cart', args=[self.produto_cimento.id]),
            {'quantidade': 1}
        )
        # Remove produto
        self.client.get(
            reverse('remove_from_cart', args=[self.produto_cimento.id])
        )
        
        session = self.client.session
        self.assertNotIn(str(self.produto_cimento.id), session.get('cart', {}))

    def test_limpar_carrinho(self):
        """Testa a funcionalidade de limpar todo o carrinho"""
        # Adiciona produtos
        self.client.post(
            reverse('add_to_cart', args=[self.produto_cimento.id]),
            {'quantidade': 2}
        )
        self.client.post(
            reverse('add_to_cart', args=[self.produto_areia.id]),
            {'quantidade': 3}
        )
        # Limpa carrinho
        self.client.get(reverse('clear_cart'))
        
        session = self.client.session
        self.assertEqual(session.get('cart', {}), {})

    def test_finalizar_compra_redirect(self):
        """Testa se a finalização da compra redireciona corretamente"""
        # Adiciona produto
        self.client.post(
            reverse('add_to_cart', args=[self.produto_cimento.id]),
            {'quantidade': 1}
        )
        # Finaliza compra
        response = self.client.get(reverse('finalizar_compra'))
        
        self.assertRedirects(response, reverse('checkout'))


if __name__ == '__main__':
    unittest.main()
