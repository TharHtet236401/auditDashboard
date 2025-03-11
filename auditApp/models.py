from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.

class Transaction(models.Model):
    status = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],null=False, blank=False)
    status = models.CharField(max_length=255, choices=status, null=False, blank=False,default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)
    merchant =models.CharField(max_length=255, null=False, blank=False)
    isFlagged = models.BooleanField(default=False,null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)



    def __str__(self):
        return f"{self.merchant} - {self.amount} - {self.status}"
