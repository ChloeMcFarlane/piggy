from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("admin/", admin.site.urls),
    path("transactions/", views.transactions_list, name="transactions-list"),
    path("transactions/create/", views.create_transaction, name="create-transaction"),
    path("transactions/success/", views.transaction_success, name="transaction-success"),

    path("transactions/<int:ok>/update/", views.update_transaction, name='update-transaction')
]