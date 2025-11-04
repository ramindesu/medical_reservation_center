from django.db import models
from Medical_Archive.models import Specialty, History

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
        ordering = ['first_name']
        abstract = True


class Doctor(User):
    medical_code = models.CharField(max_length=30, unique=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    monthly_reservation_capacity = models.PositiveIntegerField(default=50)

    def save(self, *args, **kwargs):
        self.role = self.Role.DOCTOR
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'
        ordering = ['specialty']


class Patient(User):
    history = models.ForeignKey(History, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.role = self.Role.PATIENT
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name}-{self.last_name}'

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
        ordering = ['first_name']