from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

TRANSACTION_TYPES = (('TOP_UP','top_up'), ('WITHDRAW', 'withdraw'), ('TRANSFER', 'transfer'),)
STATUS_TYPES = (('SUCCESS','success'), ('FAILURE', 'failure'), ('PENDING', 'pending'),)

class Transaction(models.Model):
    type = models.CharField(max_length=150, choices=TRANSACTION_TYPES)
    performed_by = models.ForeignKey(User, related_name='transactions', on_delete=models.PROTECT, null=False)
    performed_on = models.ForeignKey('accounts.CustomerBankAccount', related_name='account_transactions', on_delete=models.PROTECT, null=False)
    amount = models.FloatField()
    status = models.CharField(max_length=150, choices=STATUS_TYPES)

    def __str__(self):
        return "{} Performed By {} ".format(self.type, self.performed_by.username)
