from django.db import models
from merchants.models import Merchant


class Payout(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    amount_paise = models.BigIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    # FIXED: use CharField instead of UUIDField
    idempotency_key = models.CharField(max_length=255, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payout {self.id} - {self.status}"