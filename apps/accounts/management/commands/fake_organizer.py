from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from faker import Faker

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = "Generate fake organizers"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Number of organizers to create")

    def handle(self, *args, **options):
        count = options["count"]
        for i in range(count):
            user = User.objects.order_by("?").first()
            user.is_organizer_pending = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Organizer created: {user.email}"))

        self.stdout.write(self.style.SUCCESS(f"{count} organizers created"))
