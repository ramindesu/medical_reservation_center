from django.db import models
from Accounts.models import Patient


class Specialty(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Specialty"
        verbose_name_plural = "Specialties"
        ordering = ["title"]



class History(models.Model):
    patient = models.ForeignKey('Accounts.Patient', on_delete=models.CASCADE)
    history = models.TextField()


    def __str__(self):
        return f"History for {self.patient.first_name}"

    class Meta:
        verbose_name = "Patient History"
        verbose_name_plural = "Patient Histories"
        ordering = ["patient"]