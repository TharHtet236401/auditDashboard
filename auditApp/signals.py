from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Transaction, TransactionHistory
import threading

# Store the current user in thread local storage
_local = threading.local()

def get_current_user():
    return getattr(_local, 'user', None)

def set_current_user(user):
    _local.user = user

@receiver(pre_save, sender=Transaction)
def track_transaction_changes(sender, instance, **kwargs):
    try:
        if instance.pk:  # Only track changes for existing instances
            old_instance = Transaction.objects.get(pk=instance.pk)
            
            # Fields to track
            tracked_fields = ['status', 'isFlagged', 'amount', 'merchant']
            
            for field in tracked_fields:
                old_value = getattr(old_instance, field)
                new_value = getattr(instance, field)
                
                if old_value != new_value:
                    TransactionHistory.objects.create(
                        transaction=instance,
                        changed_by=get_current_user(),
                        field_name=field,
                        old_value=str(old_value),
                        new_value=str(new_value)
                    )
    except Exception as e:
        print(f"Error tracking changes: {str(e)}") 