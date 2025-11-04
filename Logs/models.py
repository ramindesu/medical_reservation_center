from django.db import models
from Accounts.models import User, Patient
from Reservations.models import Reservation


class Log(models.Model):
    
    ACTION_CHOICES = [
        ("login", "User Login"),
        ("logout", "User Logout"),
        ("create", "Create Action"),
        ("update", "Update Action"),
        ("delete", "Delete Action"),
        ("payment", "Payment Transaction"),
        ("reservation_request", "Reservation Request"),
        ("reservation_schedule", "Reservation Scheduled"),
        ("quota_increase_request", "Quota Increase Request"),
        ("system", "System Event"),
    ]

    ACTOR_CHOICES = [
        ("admin", "Admin"),
        ("dostor", "Doctor"),
        ("patient", "Patient")
    ]
   
    info = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='logs')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    actor = models.CharField(max_length=50, choices=ACTOR_CHOICES)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"        
        ordering = ['-time']

    def __str__(self):
        user = self.info.id if self.info else "System"
        return f"{user}({self.actor}): {self.action} ({self.time:%Y-%m-%d %H:%M})"
