from django.db import models
from Accounts.models import Doctor, Patient
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, Count
from datetime import time


class Reservations(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField(default=time(9,0))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    service = models.CharField(max_length=100)

    class Status(models.TextChoices):
        WAITING = 'waiting', 'Waiting'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        CANCELED = 'canceled', 'Canceled'
        BLOCKED = 'blocked', 'Blocked'

    status = models.CharField(
        max_length=15, choices=Status.choices, default=Status.WAITING)
    

    
    @property
    def display_status(self):
       
        from Configs.models import Blacklist
        if Blacklist.objects.filter(doctor=self.doctor, patient=self.patient, active=True).exists():
            return Reservations.Status.BLOCKED
        return self.status

    def __str__(self):
        return f"Reservation: {self.patient.user.first_name} → {self.doctor.user.first_name} ({self.status})"

    class Meta:
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'


class FeedBackManager(models.Manager):
    def doctor_rating_average(self):
        return self.values("doctor_id", "doctor__user__first_name", "doctor__user__last_name", "doctor__specialty__title").annotate(
            rating_average=Avg("rating"),
            total_feedback_count=Count("id")
        ).order_by("-rating_average")

    def top_doctors(self, top_numbers=3):
        return self.doctor_rating_average()[:top_numbers]

    def low_doctors(self, low_numbers=3):
        return self.doctor_rating_average().order_by("rating_average")[:low_numbers]


class FeedBack(models.Model):
    reservation = models.ForeignKey(Reservations, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = FeedBackManager()

    def __str__(self):
        return f"Feedback ({self.rating}/10) from {self.patient.user.first_name}"

    class Meta:
        verbose_name = 'FeedBack'
        verbose_name_plural = 'FeedBacks'
        ordering = ['rating']
