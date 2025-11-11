from django.db import models


# Create your models here.


class Wallet(models.Model):
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    transaction = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Balance: {self.balance} | Transaction: {self.transaction}"

    class Meta:
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'
        ordering = ['balance']
