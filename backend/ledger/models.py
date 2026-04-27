from django.db import models
from merchants.models import Merchant

class LedgerEntry(models.Model):
    ENTRY_TYPE_CHOICES = [
        ("credit", "Credit"),
        ("debit", "Debit"),
    ]

    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    amount_paise = models.BigIntegerField()
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)