import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.utils import timezone
from tracker.models import User, Transaction, Category


class Command(BaseCommand):
    help = "Generates transactions for testing"

    def handle(self, *args, **options):
        fake = Faker()

        # Creating categories
        categories = [
            "Mortgage/Rent",
            "Utilities",
            "Gas/Transportation",
            "Food",
            "Subscriptions",
            "Entertainment",
            "Monthly Income",
            "Medical",
            "Repairs",
            "Clothing",
            "Cosmetics",
            "Memberships / Subscriptions",
            "Other",
        ]

        for category in categories:
            Category.objects.get_or_create(name=category)

        # Get or create the user
        user = User.objects.filter(username="Chloe").first()
        if not user:
            user = User.objects.create_superuser(
                username="Chloe", password="testtestpassword123"
            )

        # Generate transactions (unindented so this always runs)
        all_categories = Category.objects.all()
        types = [x[0] for x in Transaction.TRANSACTION_TYPE_CHOICES]

        for i in range(20):
            Transaction.objects.create(
                category=random.choice(all_categories),
                user=user,
                amount=round(random.uniform(1, 2500), 2),
                date=fake.date_time_between(
                    start_date="-1y",
                    end_date="now",
                    tzinfo=timezone.get_current_timezone(),
                ),
                type=random.choice(types),
            )