from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from faker import Faker
from apps.events.models import Event

User = get_user_model()

fake = Faker()


class Command(BaseCommand):
    help = "Generate fake events"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Number of events to create")

    def handle(self, *args, **options):
        count = options["count"]
        for i in range(count):
            user = User.objects.filter(is_organizer_pending=True).order_by("?").first()
            event = Event.objects.create(
                title=fake.sentence(),
                description=fake.text(),
                date=fake.date_time(),
                start_time=fake.time(),
                end_time=fake.time(),
                location=fake.address(),
                max_participants=fake.random_int(min=1, max=100),
                owner=user,
            )
            self.stdout.write(self.style.SUCCESS(f"Event created: {event.title}"))

        self.stdout.write(self.style.SUCCESS(f"{count} events created"))
