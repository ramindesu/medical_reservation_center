from django.db import models
from Accounts.models import User
from Accounts.models import User, Patient
from Reservations.models import Reservations

class Log(models.Model):

    class Action(models.TextChoices):
        LOGIN = 'login', 'Login'
        LOGIUT = 'logout', 'Logout'
        CREATE = 'create', 'Create'
        UPDATE ='update', 'Update'
        DELETE = 'delete', 'Delete'
        PAYMENT = 'payment', 'Payment'
        RESERVATION = 'reservation', 'Reservation'
        GUOTA_INCREASE = 'quota_increase', 'Quota Increase'

    class Actor(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        DOCTOR = 'dostor', 'Doctor'
        PATIENT = 'patient', 'Patient'

    info = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logs')
    action = models.CharField(max_length=50, choices=Action.choices)
    actor = models.CharField(max_length=50, choices=Actor.choices)
    time = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"        
        ordering = ['-time']

    def __str__(self):
        return f"{self.info}({self.actor}): {self.action} ({self.time:%Y-%m-%d %H:%M})"
        return f"{self.info}({self.actor}): {self.action} ({self.time:%Y-%m-%d %H:%M})"


class Transaction(models.Model):

    class Status(models.TextChoices):
        PAID = 'paid', 'Paid'
        CHARGE = 'charge', 'Charge'
        CANCELLED = 'cancelled', 'Cancelled'

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices)  
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='transactions')
    reservation = models.ForeignKey(Reservations, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions" 
        ordering = ['status']

    def __str__(self):
        return f"{User.last_name}: {self.amount} ({self.status})"