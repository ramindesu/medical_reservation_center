from django.db import models
from datetime import datetime
from Accounts.models import Doctor, Patient
from django.core.validators import MinValueValidator, MaxValueValidator

class Reservations(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    service = models.CharField(max_length=100)

    class Status(models.TextChoices):
        WAITING = 'waiting', 'Waiting'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        CANCELED = 'canceled', 'Canceled'

    status = models.CharField(max_length=15, choices=Status.choices, default=Status.WAITING)

    def __str__(self):
        return f"Reservation: {self.patient.first_name} → {self.doctor.first_name} ({self.status})"

    class Meta:
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'


class FeedBack(models.Model):
    reservation = models.ForeignKey(Reservations, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    def __str__(self):
        return f"Feedback ({self.rating}/10) from {self.patient.first_name}"
    
    class Meta:
        verbose_name = 'FeedBack'
        verbose_name_plural = 'FeedBacks'
        ordering = ['rating']


    