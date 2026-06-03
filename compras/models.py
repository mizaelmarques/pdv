from django.db import models


class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    unidade = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nome} - R${self.preco:.2f}/{self.unidade}"


class Pedido(models.Model):
    numero = models.IntegerField(unique=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    finalizado = models.BooleanField(default=False)

    def __str__(self):
        return f"Pedido #{self.numero}"

