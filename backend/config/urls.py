from django.contrib import admin
from django.urls import path
from payouts.views import create_payout, get_payout

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/payouts/', create_payout),
    path('api/v1/payouts/<int:payout_id>/', get_payout),
]