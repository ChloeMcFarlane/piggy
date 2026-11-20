from django.shortcuts import render
from django.shortcuts import render
# IMPORT FOR LOGINS
from django.contrib.auth.decorators import login_required

# IMPORT FOR MODELS
from tracker.models import Transaction

# IMPORT FOR FILTERS
from tracker.filter import TransactionFilter

def home(request):
    return render(request, 'index.html')

# Create your views here.
def index(request):
    return render(request, 'tracker/index.html')

@login_required
def transactions_list(request):
    transaction_filter = TransactionFilter(
        request.GET,
        # FOR IDEAL PERFORMANCE
        queryset=Transaction.objects.filter(user=request.user).select_related('category')
    )
    context = {'filter': transaction_filter}
    # RETURN TEMPLATE FRAGMENT
    if request.htmx:
        return render(request,'tracker/partials/transactions-container.html', context)

    return render(request,'tracker/transactions-list.html', context)
