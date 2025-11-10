from django.db import models
from Accounts.models import User  

class Log(models.Model):
    class Action(models.TextChoices):
        LOGIN = 'login', 'Login'
        LOGOUT = 'logout', 'Logout'
        CREATE = 'create', 'Create'
        UPDATE = 'update', 'Update'
        DELETE = 'delete', 'Delete'
        PAYMENT = 'payment', 'Payment'
        RESERVATION = 'reservation', 'Reservation'
        QUOTA_INCREASE = 'quota_increase', 'Quota Increase'

    class Actor(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        DOCTOR = 'doctor', 'Doctor' 
        PATIENT = 'patient', 'Patient'

    info = models.ForeignKey(
        'Accounts.User',
        on_delete=models.CASCADE,
        related_name='logs'
    )
    action = models.CharField(max_length=50, choices=Action.choices)
    actor = models.CharField(max_length=50, choices=Actor.choices)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"
        ordering = ['-time']

    def __str__(self):
        return f"{self.info.first_name} {self.info.last_name} ({self.actor}): {self.action} ({self.time:%Y-%m-%d %H:%M})"
