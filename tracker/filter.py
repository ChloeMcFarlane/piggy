import django_filters

from tracker.models import Transaction


class TransactionFilter(django_filters.FilterSet):
    transaction_type = django_filters.ChoiceFilter(
        field_name='type',
        choices=Transaction.TRANSACTION_TYPE_CHOICES,
        empty_label='Any',
    )

    class Meta:
        model = Transaction
        fields = ('transaction_type',)