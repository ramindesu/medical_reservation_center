from django.db import models
from datetime import datetime
from Accounts.models import Doctor , Patient
# Create your models here.
class Reservations(models.Model):
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    date = models.DateField()
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField()
    service = models.CharField(max_length=100)
    class Status(models.TextChoices):
        WAITING = 'waiting' , "Waiting"
        APPOROVED = 'apporoved' , 'Apporoved'
        REJECTED = 'rejected' , 'Rejected'
        CANCELED = 'canceled ' , 'Canceld'
        
    status = models.CharField(max_length=15,choices=Status.choices , default="waiting")
    def __str__(self):
        return f" patient = {self.patient.first_name } doctor = {self.doctor.first_name}"
    
    class Meta:
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'



