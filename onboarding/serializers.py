from rest_framework import serializers
from .models import Restaurant, Branch, Subscription, TaxConfig


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class TaxConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxConfig
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    branches = BranchSerializer(many=True, read_only=True)
    subscriptions = SubscriptionSerializer(many=True, read_only=True)
    tax_configs = TaxConfigSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = '__all__'


class RestaurantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'