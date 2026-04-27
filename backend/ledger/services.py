from django.db.models import Sum
from ledger.models import LedgerEntry


def get_balance(merchant):
    credits = LedgerEntry.objects.filter(
        merchant=merchant,
        entry_type="credit"
    ).aggregate(total=Sum("amount_paise"))["total"] or 0

    debits = LedgerEntry.objects.filter(
        merchant=merchant,
        entry_type="debit"
    ).aggregate(total=Sum("amount_paise"))["total"] or 0

    return credits - debits


def create_credit_entry(merchant, amount_paise):
    return LedgerEntry.objects.create(
        merchant=merchant,
        amount_paise=amount_paise,
        entry_type="credit"
    )


def create_debit_entry(merchant, amount_paise):
    return LedgerEntry.objects.create(
        merchant=merchant,
        amount_paise=amount_paise,
        entry_type="debit"
    )