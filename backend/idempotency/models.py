from django.db import models
from merchants.models import Merchant


class IdempotencyKey(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)

    # FIXED
    key = models.CharField(max_length=255)

    # FIXED
    response_data = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("merchant", "key")