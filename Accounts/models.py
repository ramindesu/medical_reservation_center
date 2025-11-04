from django.db import models
from Medical_Archive import Specialty

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField(unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    active = models.BooleanField(default=True)
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        DOCTOR = 'doctor', 'Doctor'
        PATIENT = 'patient', 'Patient'
    role = models.CharField(max_length=10, choices=Role.choices)
    def __str__(self):
        return f"{self.first_name}-{self.last_name}-{self.role}"
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['fisrtـname']
        abstract = True

class Doctor(User):
    info = models.ForeignKey(User,on_delete=models.CASCADE)
    medical_code = models.CharField(max_length=30,unique=True)
    specialty = models.ForeignKey(Specialty,on_delete=models.CASCADE)
    monthly_reservation_capacity = models.PositiveIntegerField(default=50)
    
    def __str__(self):
        return f'{self.info.first_name} - {self.info.last_name}'
    