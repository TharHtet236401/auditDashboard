from django.db import migrations
import random
import string

def generate_hex_id():
    return ''.join(random.choices(string.hexdigits.upper(), k=6))

def convert_existing_ids(apps, schema_editor):
    Transaction = apps.get_model('auditApp', 'Transaction')
    db_alias = schema_editor.connection.alias
    
    # Create a mapping of old IDs to new hex IDs
    id_mapping = {}
    for transaction in Transaction.objects.using(db_alias).all():
        while True:
            hex_id = generate_hex_id()
            if hex_id not in id_mapping.values():
                id_mapping[transaction.id] = hex_id
                break
    
    # Update transactions one by one
    for old_id, new_id in id_mapping.items():
        Transaction.objects.using(db_alias).filter(id=old_id).update(id=new_id)

def reverse_convert(apps, schema_editor):
    pass  # We don't want to reverse this migration

class Migration(migrations.Migration):
    dependencies = [
        ('auditApp', '0006_alter_transaction_id'),
    ]

    operations = [
        migrations.RunPython(convert_existing_ids, reverse_convert),
    ] 