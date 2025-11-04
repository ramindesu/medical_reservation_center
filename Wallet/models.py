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
        if self.patient:
            return f"Wallet of Patient: {self.patient.user.first_name} {self.patient.user.last_name}"
        elif self.doctor:
            return f"Wallet of Doctor: {self.doctor.user.first_name} {self.doctor.user.last_name}"
        return f"Wallet balance: {self.balance} - Transaction: {self.transaction}"

    class Meta:
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'
        ordering = ['patient__user__first_name', 'doctor__user__first_name']
