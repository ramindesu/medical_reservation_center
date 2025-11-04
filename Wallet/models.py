from django.db import models

# Create your models here.


class Wallet(models.Model):
    patient = models.OneToOneField(
        'account.Patient', on_delete=models.CASCADE, related_name='patient_wallet')
    doctor = models.OneToOneField(
        'account.Doctor', on_delete=models.CASCADE, related_name='doctor_wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    transaction = models.TextField()

    def __str__(self):
        return f"Wallet of {self.patient} and {self.doctor} with balance {self.balance}"

    def deposit(self, amount):
        self.balance += amount
        self.save()
    """یه متدی باید برای شارژ کیف پول می داشتیم که توی views صداش کنیم بعدا"""


class Transaction(models.Model):
    """مدلWallet بدون تراکنش معنا ندارد بنابراین این مدل برای ثبت تراکنش‌هااست.
   از طرفی چون  هر wallet   می‌تواند چندین تراکنش داشته باشد، رابطه ForeignKey تعریف شده است."""
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20)
    patient = models.ForeignKey(
        'auth.user', on_delete=models.CASCADE, related_name='patient_transactions')
    doctor = models.ForeignKey(
        'auth.user', on_delete=models.CASCADE, related_name='doctor_transactions')
    reservation = models.ForeignKey(
        'Reservation.Reservation', on_delete=models.CASCADE, related_name='reservation_transactions')

    def __str__(self):
        return f"Transaction of {self.amount} on {self.wallet}"
