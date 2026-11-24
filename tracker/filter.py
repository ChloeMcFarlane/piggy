import django_filters
from django import forms
from tracker.models import Transaction, Category

def user_categories(request):
    if request is None:
        return Category.objects.none()
    return Category.objects.filter(transaction__user=request.user).distinct()

class TransactionFilter(django_filters.FilterSet):
    transaction_type = django_filters.ChoiceFilter(
        field_name='type',
        choices=Transaction.TRANSACTION_TYPE_CHOICES,
        empty_label='Any',
    )

    start_date = django_filters.DateFilter(
    field_name='date__date',
    lookup_expr='gte',
    label='Date From',
    widget=forms.DateInput(attrs={'type': 'date'}),
    )

    end_date = django_filters.DateFilter(
        field_name='date__date',
        lookup_expr='lte',
        label='Date To',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    category = django_filters.ModelMultipleChoiceFilter(
    queryset=user_categories,
    widget=forms.CheckboxSelectMultiple(),
    label='Categories',
    )

    class Meta:
        model = Transaction
        fields = ('transaction_type', 'start_date', 'end_date', 'category')