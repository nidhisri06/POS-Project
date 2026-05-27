from rest_framework import serializers
from .models import (
    Customer, MembershipPlan, CustomerMembership,
    LoyaltyTransaction, CustomerOrderHistory,
    Campaign, CustomerFeedback, PersonalizedOffer
)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class MembershipPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipPlan
        fields = '__all__'


class CustomerMembershipSerializer(serializers.ModelSerializer):
    plan_name = serializers.CharField(source='plan.name', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = CustomerMembership
        fields = '__all__'


class LoyaltyTransactionSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = LoyaltyTransaction
        fields = '__all__'


class CustomerOrderHistorySerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = CustomerOrderHistory
        fields = '__all__'


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'


class CustomerFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerFeedback
        fields = '__all__'


class PersonalizedOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalizedOffer
        fields = '__all__'


class CustomerDetailSerializer(serializers.ModelSerializer):
    """Full customer profile with loyalty, membership and order history"""
    loyalty_transactions = LoyaltyTransactionSerializer(many=True, read_only=True)
    order_history = CustomerOrderHistorySerializer(many=True, read_only=True)
    membership = CustomerMembershipSerializer(read_only=True)
    offers = PersonalizedOfferSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'

from .models import (
    Customer, MembershipPlan, CustomerMembership,
    LoyaltyTransaction, CustomerOrderHistory,
    Campaign, CustomerFeedback, PersonalizedOffer, Notification
)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'