from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from django.shortcuts import get_object_or_404

from merchants.models import Merchant
from ledger.services import get_balance, create_debit_entry
from payouts.models import Payout
from payouts.tasks import process_payout
from idempotency.models import IdempotencyKey


@api_view(['POST'])
def create_payout(request):
    merchant_id = request.data.get('merchant_id')
    amount = request.data.get('amount_paise')
    idempotency_key = request.headers.get('Idempotency-Key') or request.data.get('idempotency_key')

    # Basic validation
    if not merchant_id or not amount or not idempotency_key:
        return Response({"error": "Invalid input"}, status=400)

    #  Safe amount parsing
    try:
        amount = int(amount)
    except (ValueError, TypeError):
        return Response({"error": "Invalid amount"}, status=400)

    if amount <= 0:
        return Response({"error": "Amount must be positive"}, status=400)

    with transaction.atomic():
        #  Lock merchant row
        merchant = get_object_or_404(
            Merchant.objects.select_for_update(),
            id=merchant_id
        )

        #  Idempotency check
        existing = IdempotencyKey.objects.filter(
            merchant=merchant,
            key=idempotency_key
        ).first()

        if existing:
            return Response(existing.response_data)

        #  Check balance
        balance = get_balance(merchant)
        if balance < amount:
            return Response({"error": "Insufficient balance"}, status=400)

        #  Create payout
        payout = Payout.objects.create(
            merchant=merchant,
            amount_paise=amount,
            status='pending',
            idempotency_key=idempotency_key
        )

        #  Deduct money
        create_debit_entry(merchant, amount)

        response_data = {
            "status": "pending",
            "payout_id": payout.id
        }

        # 🔥 FINAL FIX (THIS WAS YOUR ERROR)
        IdempotencyKey.objects.create(
            merchant=merchant,   # REQUIRED
            key=idempotency_key,
            response_data=response_data
        )

    # Trigger async task
    process_payout.delay(payout.id)

    return Response(response_data)


@api_view(['GET'])
def get_payout(request, payout_id):
    try:
        payout = Payout.objects.get(id=payout_id)
        return Response({
            "id": payout.id,
            "status": payout.status,
            "amount": payout.amount_paise
        })
    except Payout.DoesNotExist:
        return Response({"error": "Not found"}, status=404)