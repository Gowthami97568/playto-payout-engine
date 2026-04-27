import random
import time
from django.db import transaction
from payouts.models import Payout
from ledger.models import LedgerEntry

MAX_RETRIES = 3

def process_payouts():
    payouts = Payout.objects.filter(status='pending')[:10]

    for payout in payouts:
        with transaction.atomic():
            p = Payout.objects.select_for_update().get(id=payout.id)

            if p.status != 'pending':
                continue

            p.status = 'processing'
            p.save()

        time.sleep(1)
        success = random.choice([True, False])

        with transaction.atomic():
            p = Payout.objects.select_for_update().get(id=payout.id)

            if success:
                p.status = 'completed'
                p.save()
            else:
                p.retry_count += 1

                if p.retry_count >= MAX_RETRIES:
                    p.status = 'failed'

                    # refund
                    LedgerEntry.objects.create(
                        merchant=p.merchant,
                        amount_paise=p.amount_paise,
                        entry_type='credit',
                        reference_id=p.id
                    )
                else:
                    p.status = 'pending'

                p.save()