from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
import random
import string


# Create your models here.

def get_unique_hex_id():
    while True:
        hex_id = ''.join(random.choices(string.hexdigits.upper(), k=6))
        if not Transaction.objects.filter(id=hex_id).exists():
            return hex_id

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('Approved', 'Approved'),
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected'),
    ]
    id = models.CharField(primary_key=True, max_length=6, default=get_unique_hex_id, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],null=False, blank=False)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, null=False, blank=False,default='Pending')
    timestamp = models.DateTimeField(auto_now_add=True)
    merchant = models.CharField(max_length=255, null=False, blank=False)
    isFlagged = models.BooleanField(default=False,null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.merchant} - {self.amount} - {self.status}"

    def get_history(self):
        return self.history.all().select_related('changed_by').order_by('-changed_at')

class TransactionHistory(models.Model):
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE, related_name='history')
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    field_name = models.CharField(max_length=100)
    old_value = models.CharField(max_length=255, null=True)
    new_value = models.CharField(max_length=255, null=True)

    class Meta:
        ordering = ['-changed_at']

    def __str__(self):
        return f"{self.field_name} changed from {self.old_value} to {self.new_value}"
