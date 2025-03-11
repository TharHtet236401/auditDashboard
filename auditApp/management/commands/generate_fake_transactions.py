from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from auditApp.models import Transaction
from faker import Faker
import random
from decimal import Decimal

class Command(BaseCommand):
    help = 'Generate fake transactions for testing'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of fake transactions to create')

    def handle(self, *args, **kwargs):
        try:
            count = kwargs['count']
            fake = Faker()
            
            # Get all users for random assignment
            users = list(User.objects.all())
            if not users:
                self.stdout.write(
                    self.style.ERROR('No users found. Please create some users first using generate_fake_users command.')
                )
                return
            
            # Common merchant types
            merchant_types = [
                'Restaurant', 'Retail Store', 'Online Shop', 'Supermarket', 
                'Gas Station', 'Electronics Store', 'Department Store',
                'Hotel', 'Airlines', 'Pharmacy'
            ]
            
            # Generate transactions
            for i in range(count):
                # Generate random amount between $1 and $10000
                amount = round(random.uniform(1, 10000), 2)
                
                # Create merchant name
                merchant_type = random.choice(merchant_types)
                merchant_name = f"{fake.company()} {merchant_type}"
                
                # Random status with weighted choices
                status = random.choices(
                    ['Approved', 'Pending', 'Rejected'],
                    weights=[0.6, 0.3, 0.1]  # 60% Approved, 30% Pending, 10% Rejected
                )[0]
                
                # Random flag status (20% chance of being flagged)
                is_flagged = random.random() < 0.2
                
                # Create transaction
                transaction = Transaction.objects.create(
                    amount=Decimal(str(amount)),
                    merchant=merchant_name,
                    status=status,
                    isFlagged=is_flagged
                )
                
                # If status is approved, assign a random user as approver
                if status == 'Approved':
                    transaction.approved_by = random.choice(users)
                    transaction.save()
                
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created transaction: {transaction}')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating transactions: {str(e)}')
            ) 