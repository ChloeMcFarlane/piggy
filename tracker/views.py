from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from tracker.models import Transaction
from tracker.filter import TransactionFilter
from tracker.forms import TransactionForm


def home(request):
    return render(request, 'index.html')


def index(request):
    return render(request, 'tracker/index.html')


@login_required
def transactions_list(request):
    transaction_filter = TransactionFilter(
        request.GET,
        request=request,
        queryset=Transaction.objects.filter(user=request.user).select_related('category')
    )
    total_income = transaction_filter.qs.get_total_income()
    total_expenses = transaction_filter.qs.get_total_expenses()

    context = {
        'filter': transaction_filter,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_income': total_income - total_expenses,
    }

    if request.htmx and not request.htmx.history_restore_request:
        response = render(request, 'tracker/partials/transactions-container.html', context)
    else:
        response = render(request, 'tracker/transactions-list.html', context)

    response['Vary'] = 'HX-Request'
    return response


@login_required
@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            request.session['success_message'] = "Transaction was added successfully!"
            return redirect('transaction-success')
    else:
        form = TransactionForm()

    return render(request, 'tracker/partials/create_transaction.html', {'form': form})


@login_required
def transaction_success(request):
    message = request.session.pop('success_message', None)
    if message is None:
        return redirect('transactions-list')
    return render(request, 'tracker/partials/transaction-success.html', {'message': message})