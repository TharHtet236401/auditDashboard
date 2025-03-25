import random
import string
from django.core.management.base import BaseCommand
from auditApp.models import Transaction, TransactionHistory
from django.db import transaction

class Command(BaseCommand):
    help = 'Fix transaction IDs and their relationships'

    def generate_hex_id(self):
        return ''.join(random.choices(string.hexdigits.upper(), k=6))

    def handle(self, *args, **options):
        with transaction.atomic():
            # Get all transactions and their related history
            transactions = Transaction.objects.all()
            self.stdout.write(f'Found {transactions.count()} transactions to process')

            # Create mapping of old to new IDs
            id_mapping = {}
            
            # Generate new hex IDs
            for t in transactions:
                while True:
                    hex_id = self.generate_hex_id()
                    if hex_id not in id_mapping.values():
                        id_mapping[t.id] = hex_id
                        break

            # Update transaction history records first
            for old_id, new_id in id_mapping.items():
                TransactionHistory.objects.filter(transaction_id=old_id).update(transaction_id=new_id)
                self.stdout.write(f'Updated history records for transaction {old_id} to {new_id}')

            # Then update transactions
            for old_id, new_id in id_mapping.items():
                Transaction.objects.filter(id=old_id).update(id=new_id)
                self.stdout.write(f'Updated transaction {old_id} to {new_id}') 