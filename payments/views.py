from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from onboarding.models import Restaurant, Subscription
from .models import Payment
from .services import client


PLAN_PRICES = {
    "basic": 19,
    "standard": 49,
    "premium": 99
}


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_subscription_order(request):

    restaurant_id = request.data.get('restaurant_id')
    plan = request.data.get('plan')

    if not restaurant_id or not plan:
        return Response({
            "error": "restaurant_id and plan required"
        }, status=400)

    if plan not in PLAN_PRICES:
        return Response({
            "error": "Invalid subscription plan"
        }, status=400)

    amount = PLAN_PRICES[plan] * 100

    razorpay_order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    restaurant = Restaurant.objects.get(id=restaurant_id)

    payment = Payment.objects.create(
        restaurant=restaurant,
        plan_name=plan,
        amount=PLAN_PRICES[plan],
        razorpay_order_id=razorpay_order['id'],
        status='created'
    )

    return Response({
        "key": settings.RAZORPAY_KEY_ID,
        "amount": amount,
        "currency": "INR",
        "order_id": razorpay_order['id'],
        "plan": plan
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_subscription_payment(request):

    data = request.data

    try:

        client.utility.verify_payment_signature({
            'razorpay_order_id':
                data['razorpay_order_id'],

            'razorpay_payment_id':
                data['razorpay_payment_id'],

            'razorpay_signature':
                data['razorpay_signature']
        })

        payment = Payment.objects.get(
            razorpay_order_id=data['razorpay_order_id']
        )

        payment.razorpay_payment_id = data['razorpay_payment_id']
        payment.razorpay_signature = data['razorpay_signature']
        payment.status = 'paid'
        payment.save()

        Subscription.objects.create(
            restaurant=payment.restaurant,
            plan=payment.plan_name,
            status='active',
            starts_at=timezone.now(),
            expires_at=timezone.now() + timedelta(days=30),
            auto_renew=False,
            gateway_ref=data['razorpay_payment_id'],
            amount=payment.amount
        )

        return Response({
            "message": "Payment verified successfully"
        })

    except Exception as e:

        return Response({
            "error": str(e)
        }, status=400)