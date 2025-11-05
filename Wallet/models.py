from django.db import models
from Accounts.models import Doctor, Patient

# Create your models here.


class Wallet(models.Model):
    patient = models.OneToOneField(
        Patient, on_delete=models.CASCADE, related_name='patient_wallet', null=True, blank=True)
    doctor = models.OneToOneField(
        Doctor, on_delete=models.CASCADE, related_name='doctor_wallet', null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    transaction = models.TextField()

    def __str__(self):
        if self.patient:
            return f"Wallet of Patient: {self.patient.first_name} {self.patient.last_name}"
        elif self.doctor:
            return f"Wallet of Doctor: {self.doctor.first_name} {self.doctor.last_name}"
        return f"Wallet balance: {self.balance} - Transaction: {self.transaction}"

    class Meta:
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'
        ordering = ['patient__last_name', 'doctor__last_name']
