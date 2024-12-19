from django.db import models
from django.contrib.auth.models import User
from doctor.models import Doctor

class Payment(models.Model):
    PACKAGE_TYPES = [
        ('regular', 'Regular'),
        ('1day', '1 Day'),
        ('3day', '3 Days'),
        ('7day', '7 Days'),
    ]

    PAYMENT_METHODS = [
        ('virtual_account', 'Virtual account'),
        ('bank_transfer', 'Bank transfer'),
        ('card', 'Credit/debit card'),
    ]

    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    package_type = models.CharField(max_length=10, choices=PACKAGE_TYPES)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    admin_fee = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
