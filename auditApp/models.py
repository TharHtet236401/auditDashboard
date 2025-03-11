from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('Approved', 'Approved'),
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected'),
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],null=False, blank=False)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, null=False, blank=False,default='Pending')
    timestamp = models.DateTimeField(auto_now_add=True)
    merchant = models.CharField(max_length=255, null=False, blank=False)
    isFlagged = models.BooleanField(default=False,null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.merchant} - {self.amount} - {self.status}"
