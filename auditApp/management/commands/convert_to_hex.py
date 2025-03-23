from django.core.management.base import BaseCommand
from auditApp.models import Transaction, TransactionHistory
import random
import string
from django.db import transaction

class Command(BaseCommand):
    help = 'Convert existing transaction IDs to hexadecimal format'

    def generate_hex_id(self):
        return ''.join(random.choices(string.hexdigits.upper(), k=6))

    def handle(self, *args, **options):
        with transaction.atomic():
            # Create a mapping of old IDs to new hex IDs
            id_mapping = {}
            transactions = Transaction.objects.all()
            
            # First, generate all new IDs
            for t in transactions:
                while True:
                    hex_id = self.generate_hex_id()
                    if hex_id not in id_mapping.values():
                        id_mapping[t.id] = hex_id
                        break
            
            # Update each transaction and its history records
            for old_id, new_id in id_mapping.items():
                # Update the transaction's history records first
                TransactionHistory.objects.filter(transaction_id=old_id).update(transaction_id=new_id)
                # Then update the transaction itself
                Transaction.objects.filter(id=old_id).update(id=new_id)

            self.stdout.write(self.style.SUCCESS(f'Successfully converted {len(id_mapping)} transaction IDs to hexadecimal format')) 