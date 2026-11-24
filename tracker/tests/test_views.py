import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from tracker.models import Category

@pytest.mark.django_db
def test_total_values_appear_on_list_page(user_transactions, client):
    user = user_transactions[0].user
    client.force_login(user)

    income_total = sum(t.amount for t in user_transactions if t.type == 'income')
    expense_total = sum(t.amount for t in user_transactions if t.type == 'expense')
    net = income_total - expense_total

    response = client.get(reverse('transactions-list'))
    assert response.context['total_expenses'] == expense_total
    assert response.context['total_income'] == income_total
    assert response.context['net_income'] == net

@pytest.mark.django_db
def test_transaction_type_filter(user_transactions, client):
    user = user_transactions[0].user
    client.force_login(user)

    # income check
    response = client.get(reverse('transactions-list'), {'transaction_type': 'income'})
    qs = response.context['filter'].qs
    assert qs.count() > 0
    assert all(t.type == 'income' for t in qs)

    # expense check
    response = client.get(reverse('transactions-list'), {'transaction_type': 'expense'})
    qs = response.context['filter'].qs
    assert qs.count() > 0
    assert all(t.type == 'expense' for t in qs)

    for transaction in qs:
        assert transaction.type == 'expense'


@pytest.mark.django_db
def test_start_and_end_date(user_transactions, client):
    user = user_transactions[0].user
    client.force_login(user)

    start_date_cutoff = timezone.localdate() - timedelta(days=120)
    response = client.get(reverse('transactions-list'), {'start_date': start_date_cutoff})

    qs = response.context['filter'].qs
    assert qs.count() > 0
    for transaction in qs:
        assert timezone.localtime(transaction.date).date() >= start_date_cutoff

    end_date_cutoff = timezone.localdate() - timedelta(days=20)
    response = client.get(reverse('transactions-list'), {'end_date': end_date_cutoff})

    qs = response.context['filter'].qs
    assert qs.count() > 0
    for transaction in qs:
        assert timezone.localtime(transaction.date).date() <= end_date_cutoff


@pytest.mark.django_db
def test_category_filter(user_transactions, client):
    user = user_transactions[0].user
    client.force_login(user)

    category_pks = list(
        {t.category.pk for t in user_transactions}
    )[:2]

    response = client.get(reverse('transactions-list'), {'category': category_pks})
    qs = response.context['filter'].qs

    assert qs.count() > 0 
    assert all(t.category_id in category_pks for t in qs)






