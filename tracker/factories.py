from datetime import datetime
from django.utils import timezone
import factory

from tracker.models import Category, Transaction, User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Sequence(lambda n: 'user%d' % n)

class CategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Category
        django_get_or_create =('name',)

    name = factory.Iterator(
        [
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
    )

class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta: 
        model = Transaction

    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    amount = 5
    date = factory.Faker(
        'date_time_between',
        start_date=datetime(year=2022, month=1, day=1),
        end_date=datetime.now(),
        tzinfo=timezone.get_current_timezone(),
    )

    type = factory.Iterator(
        [
            x[0] for x in Transaction.TRANSACTION_TYPE_CHOICES
        ]
    )


    