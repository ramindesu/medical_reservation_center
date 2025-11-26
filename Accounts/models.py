from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator , MaxLengthValidator
from Wallet.models import Wallet
from django.utils import timezone
from django.db.models import Avg


class User(AbstractUser):
    address = models.TextField(null=True, blank=True, default="")
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                r"^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$",
                message="phone is not valid",
            ),
            MaxLengthValidator(20),
        ],
    )
    active = models.BooleanField(default=True)
    rate = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)], default=0
    )

    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        DOCTOR = "doctor", "Doctor"
        PATIENT = "patient", "Patient"

    role = models.CharField(max_length=10, choices=Role.choices)

    @property
    def average_rate(self):

        if self.is_doctor():
            try:
                doctor = self.doctor 

                from Reservations.models import Feedback
                result = Feedback.objects.filter(doctor=doctor).aggregate(avg_rate=Avg('rate'))
                return result['avg_rate'] or 0
            except Doctor.DoesNotExist:
                return 0
        else:

            result = User.objects.aggregate(avg_rate=Avg('rate'))
            return result['avg_rate'] or 0



    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

    def is_admin(self):
        return self.role == self.Role.ADMIN

    def is_doctor(self):
        return self.role == self.Role.DOCTOR

    def is_patient(self):
        return self.role == self.Role.PATIENT

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = User.Role.ADMIN
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["first_name"]


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    medical_code = models.CharField(max_length=30, unique=True)
    specialty = models.ForeignKey("Medical_Archive.Specialty", on_delete=models.CASCADE)
    monthly_reservation_capacity = models.PositiveIntegerField(default=50)
    wallet = models.OneToOneField(
        Wallet, on_delete=models.CASCADE, blank=True, null=True
    )
    avatar = models.ImageField(upload_to="Avatar/", blank=True, null=True)

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
    wallet = models.OneToOneField(
        Wallet, on_delete=models.CASCADE, blank=True, null=True
    )
    monthly_appointment_limit = models.IntegerField(default=5)

    def get_approved_appointments_count(self, month=None, year=None):
        if not month:
            month = timezone.now().month
        if not year:
            year = timezone.now().year

        from Reservations.models import Reservations

        return Reservations.objects.filter(
            patient=self, status="approved", date__month=month, date__year=year
        ).count()

    def can_make_appointment(self):
        return self.get_approved_appointments_count() < self.monthly_appointment_limit

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


# class Admin(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     def save(self, *args, **kwargs):
#         self.user.role = User.Role.ADMIN
#         self.user.save()
#         super().save(*args, **kwargs)

#     class Meta:
#         verbose_name = "Admin"
#         verbose_name_plural = "Admins"
