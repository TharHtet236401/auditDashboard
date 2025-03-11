from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Generate fake users for testing'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of fake users to create')

    def handle(self, *args, **kwargs):
        try:
            count = kwargs['count']
            fake = Faker()
            
            for i in range(count):
                username = fake.user_name()
                email = fake.email()
                password = fake.password(length=10)
                first_name = fake.first_name()
                last_name = fake.last_name()
                
                # Create user with basic info
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                
                # Randomly make some users staff or superuser
                if random.random() < 0.1:  # 10% chance to be staff
                    user.is_staff = True
                    if random.random() < 0.3:  # 30% of staff (3% overall) to be superuser
                        user.is_superuser = True
                    user.save()
                
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created user: {username}')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating users: {str(e)}')
            ) 