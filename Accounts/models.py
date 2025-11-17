from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from Wallet.models import Wallet


class User(AbstractUser):
    address = models.TextField()
    phone = models.CharField(max_length=15)
    active = models.BooleanField(default=True)
    rate = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], default=0)

    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        DOCTOR = "doctor", "Doctor"
        PATIENT = "patient", "Patient"

    role = models.CharField(max_length=10, choices=Role.choices)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["first_name"]


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    medical_code = models.CharField(max_length=30, unique=True)
    specialty = models.ForeignKey('Medical_Archive.Specialty', on_delete=models.CASCADE)
    monthly_reservation_capacity = models.PositiveIntegerField(default=50)
    wallet = models.OneToOneField(Wallet , on_delete=models.CASCADE, blank=True, null=True)
    avatar = models.ImageField(upload_to='Avatar/', blank=True, null=True)

    def save(self, *args, **kwargs):
        self.user.role = User.Role.DOCTOR
        self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Dr. {self.user.first_name}"

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"
        ordering = ["specialty"]


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    wallet = models.OneToOneField(Wallet,on_delete=models.CASCADE, blank=True, null=True)
    monthly_limit = models.IntegerField(default=5)
    
    def save(self, *args, **kwargs):
        self.user.role = User.Role.PATIENT
        self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.first_name}"

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        # ordering = ["first_name"]


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    def save(self, *args, **kwargs):
        self.user.role = User.Role.ADMIN
        self.user.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Admin"
        verbose_name_plural = "Admins"