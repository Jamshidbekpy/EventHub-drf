from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker

User = get_user_model()

class Command(BaseCommand):
    help = 'Generate fake users'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of users to create')

    def handle(self, *args, **options):
        count = options['count']
        fake = Faker()
        for i in range(count):
            user = User.objects.create_user(
                email=fake.email(),
                password=fake.password(),
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            self.stdout.write(self.style.SUCCESS(f'User created: {user.email}'))

        self.stdout.write(self.style.SUCCESS(f'{count} users created'))
        