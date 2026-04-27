from django.test import TestCase
from merchants.models import Merchant
from ledger.models import LedgerEntry
from ledger.services import get_balance
from django.urls import reverse
from rest_framework.test import APIClient


class PayoutTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.merchant = Merchant.objects.create(name="Test Merchant")

        # Add initial balance
        LedgerEntry.objects.create(
            merchant=self.merchant,
            amount_paise=10000,
            entry_type='credit'
        )

    # ✅ TEST 1: Ledger Balance
    def test_balance_calculation(self):
        LedgerEntry.objects.create(
            merchant=self.merchant,
            amount_paise=2000,
            entry_type='hold'
        )

        balance = get_balance(self.merchant)
        self.assertEqual(balance, 8000)

    # ✅ TEST 2: Create Payout
    def test_create_payout(self):
        response = self.client.post(
            "/api/v1/payouts",
            {
                "merchant_id": self.merchant.id,
                "amount_paise": 2000,
                "bank_account_id": "ACC123"
            },
            format='json',
            HTTP_IDEMPOTENCY_KEY="test123"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "pending")

    # ✅ TEST 3: Idempotency
    def test_idempotency(self):
        headers = {"HTTP_IDEMPOTENCY_KEY": "samekey"}

        r1 = self.client.post(
            "/api/v1/payouts",
            {
                "merchant_id": self.merchant.id,
                "amount_paise": 2000,
                "bank_account_id": "ACC123"
            },
            format='json',
            **headers
        )

        r2 = self.client.post(
            "/api/v1/payouts",
            {
                "merchant_id": self.merchant.id,
                "amount_paise": 2000,
                "bank_account_id": "ACC123"
            },
            format='json',
            **headers
        )

        self.assertEqual(r1.data["payout_id"], r2.data["payout_id"])

# Create your tests here.
