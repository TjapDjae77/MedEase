from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    @property
    def full_name(self):
        if self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.first_name

    def get_gender_display_name(self):
        return dict(self.GENDER_CHOICES)[self.gender]

    def __str__(self):
        return f"{self.full_name} - ({self.get_gender_display_name()})"
