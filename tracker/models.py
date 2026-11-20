# Authentication imports
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
# Models import
from django.db import models
# Date/Time import
from django.utils import timezone
# Import QuerySets from managers.py
from .managers import TransactionQuerySet


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Transaction(models.Model):
    # transaction can be either an INCOME or EXPENSE
    # has A CATEGORY (fx)
    # is tied to a user (FK)
    # has a DATE

    TRANSACTION_TYPE_CHOICES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )
    
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    objects = TransactionQuerySet.as_manager()

    def __str__(self):
        return f"{self.type} of {self.amount} on {self.date} by {self.user}"

    class Meta:
        ordering = ['-date']