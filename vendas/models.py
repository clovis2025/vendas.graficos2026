from django.db import models

class Venda(models.Model):
    vendedor = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.vendedor} - {self.valor}"