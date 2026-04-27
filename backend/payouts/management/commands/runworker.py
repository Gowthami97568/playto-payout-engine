from django.core.management.base import BaseCommand
from payouts.worker import process_payouts
import time

class Command(BaseCommand):
    help = "Run payout worker"

    def handle(self, *args, **kwargs):
        self.stdout.write("Worker started...")
        while True:
            process_payouts()
            time.sleep(5)