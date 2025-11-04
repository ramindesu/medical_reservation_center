from django.db import models

# Create your models here.


class Wallet(models.Model):
    patient = models.OneToOneField(
        'Accounts.Patient', on_delete=models.CASCADE, related_name='patient_wallet')
    doctor = models.OneToOneField(
        'Accounts.Doctor', on_delete=models.CASCADE, related_name='doctor_wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    transaction = models.TextField()

    def __str__(self):
        return f"Wallet of {self.patient} and {self.doctor} with balance {self.balance}"

    class Meta:
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'
        ordering = ['user.username']
