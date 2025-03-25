import random
import string
from django.db import migrations, models
import auditApp.models

def convert_to_hex(apps, schema_editor):
    # Get the historical version of the model
    Transaction = apps.get_model('auditApp', 'Transaction')
    TransactionHistory = apps.get_model('auditApp', 'TransactionHistory')
    
    # Create mapping of old to new IDs
    id_mapping = {}
    
    # First, get all existing transactions and their related history records
    transactions = Transaction.objects.all()
    
    # Generate new hex IDs for each transaction
    for transaction in transactions:
        while True:
            hex_id = ''.join(random.choices(string.hexdigits.upper(), k=6))
            if hex_id not in id_mapping.values():
                id_mapping[transaction.id] = hex_id
                break
    
    # Update the records within a single transaction
    db_alias = schema_editor.connection.alias
    
    # First, update all transaction IDs
    for old_id, new_id in id_mapping.items():
        Transaction.objects.using(db_alias).filter(id=old_id).update(id=new_id)
        # Immediately update related history records
        TransactionHistory.objects.using(db_alias).filter(transaction_id=old_id).update(transaction_id=new_id)

def reverse_convert(apps, schema_editor):
    pass  # We don't want to reverse this migration

class Migration(migrations.Migration):
    atomic = True  # Ensure the entire migration runs in a transaction
    
    dependencies = [
        ('auditApp', '0006_alter_transaction_id'),
    ]

    operations = [
        migrations.RunPython(convert_to_hex, reverse_convert),
    ] 