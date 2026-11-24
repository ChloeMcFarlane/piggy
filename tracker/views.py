from django.shortcuts import render
from django.shortcuts import render, redirect
# IMPORT FOR LOGINS
from django.contrib.auth.decorators import login_required

# IMPORT FOR MODELS
from tracker.models import Transaction

# IMPORT FOR FILTERS
from tracker.filter import TransactionFilter

# FORM IMPORT
from tracker.forms import TransactionForm

# HTMX AND HTTP IMPORTS
from django.http import HttpResponse
from django.urls import reverse


def home(request):
    return render(request, 'index.html')

# Create your views here.
def index(request):
    return render(request, 'tracker/index.html')

@login_required
def transactions_list(request):
    transaction_filter = TransactionFilter(
        request.GET,
        request=request,
        # FOR IDEAL PERFORMANCE
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

    # RETURN TEMPLATE FRAGMENT
    if request.htmx and not request.htmx.history_restore_request:
        response = render(request, 'tracker/partials/transactions-container.html', context)
    else:
        response = render(request, 'tracker/transactions-list.html', context)

    response['Vary'] = 'HX-Request'
    return response


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

            if request.htmx:
                response = HttpResponse()
                response['HX-Redirect'] = reverse('transactoin-success')
                return response
            return redirect('transaction-success')
    else:
        form = TransactionForm()

    context = {'form' : form}

    if request.htmx and not request.htmx.history_restore_request:
        return render(request, 'tracker/partials/create_transaction.html', context)
    
    return render(request, 'tracker/partials/create_transaction.html', context)




@login_required
def transaction_success(request):
    message = request.session.pop('success_message', None)
    if message is None:
        return redirect('transactions-list')
    return render(request, 'tracker/transaction_success.html', {'message': message})

    