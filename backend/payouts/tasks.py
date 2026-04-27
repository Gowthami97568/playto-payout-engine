from celery import shared_task
from django.db import transaction
import random

from payouts.models import Payout
from ledger.services import create_credit_entry


@shared_task(bind=True, max_retries=3)
def process_payout(self, payout_id):
    try:
        with transaction.atomic():
            payout = Payout.objects.select_for_update().get(id=payout_id)

            # Prevent re-processing
            if payout.status not in ["pending", "processing"]:
                return

            payout.status = "processing"
            payout.save()

        # Simulate external API (outside lock)
        outcome = random.random()

        with transaction.atomic():
            payout = Payout.objects.select_for_update().get(id=payout_id)

            if outcome < 0.7:
                payout.status = "completed"

            elif outcome < 0.9:
                payout.status = "failed"

                # ✅ Refund using correct ledger method
                create_credit_entry(payout.merchant, payout.amount_paise)

            else:
                raise self.retry(countdown=5)

            payout.save()

    except Exception as e:
        raise self.retry(exc=e, countdown=5)