from django.urls import path

from .views import (
    create_subscription_order,
    verify_subscription_payment
)

urlpatterns = [

    path(
        'create-order/',
        create_subscription_order
    ),

    path(
        'verify-payment/',
        verify_subscription_payment
    ),
]