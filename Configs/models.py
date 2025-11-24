from django.db import models
from Accounts.models import  Doctor , Patient
from Reservations.models import Reservations

class Config(models.Model):
    key = models.CharField(max_length=255 , unique=True)
    value = models.TextField(blank = True)
    description = models.TextField(blank = True , null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.key} : {self.value}"

    class Meta:
        verbose_name = "Config"
        verbose_name_plural = "Configs"
        ordering = ["key"]
        

class Blacklist(models.Model):
    doctor = models.ForeignKey(Doctor , on_delete=models.CASCADE , related_name='blacklisted_patients')
    patient = models.ForeignKey(Patient , on_delete=models.CASCADE , related_name='blacklisting_doctors')
    reason = models.TextField()
    active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('doctor' , 'patient')
        verbose_name = 'Blacklist entry'
        verbose_name_plural = 'Blacklist entries'
        
    def __str__(self):
        return f"{self.patient} blocked by {self.doctor} ({'Active' if self.active else 'Inactive'})"

class ReservationBlock(models.Model):
    reservation = models.OneToOneField(Reservations, on_delete=models.CASCADE)
    reason = models.TextField()
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Reservation {self.reservation.id} blocked ({'Active' if self.active else 'Inactive'})"


