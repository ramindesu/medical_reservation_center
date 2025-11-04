from django.db import models

# Create your models here.



class MedicalSpecialty(models.Model):
    specialty_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    

class History(models.Model):
    history_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    history = models.TextField()

    def __str__(self):
        return f"History {self.history_id} for {self.patient}" 
    
