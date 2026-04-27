# Payout Engine – Technical Explainer

---

## 1. The Ledger

### Balance Calculation Query

```python
from django.db.models import Sum

balance = LedgerEntry.objects.filter(merchant=merchant).aggregate(
    credits=Sum('amount', filter=Q(type='credit')),
    debits=Sum('amount', filter=Q(type='debit'))
)

final_balance = (balance['credits'] or 0) - (balance['debits'] or 0)