from django.urls import path
from .views import create_payout

urlpatterns = [
    path('', create_payout, name='create_payout'),
]