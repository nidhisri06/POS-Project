from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from .models import Restaurant, Branch, Subscription, TaxConfig
from .serializers import (
    RestaurantSerializer, RestaurantCreateSerializer,
    BranchSerializer, SubscriptionSerializer, TaxConfigSerializer
)


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email', 'mobile']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RestaurantCreateSerializer
        return RestaurantSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()

    @action(detail=True, methods=['patch'], url_path='toggle-active')
    def toggle_active(self, request, pk=None):
        restaurant = self.get_object()
        restaurant.is_active = not restaurant.is_active
        restaurant.save()
        return Response({'is_active': restaurant.is_active})


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

    def get_queryset(self):
        restaurant_id = self.request.query_params.get('restaurant_id')
        if restaurant_id:
            return Branch.objects.filter(restaurant_id=restaurant_id)
        return super().get_queryset()


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        restaurant_id = self.request.query_params.get('restaurant_id')
        if restaurant_id:
            return Subscription.objects.filter(restaurant_id=restaurant_id)
        return super().get_queryset()

    @action(detail=False, methods=['get'], url_path='active')
    def active_subscriptions(self, request):
        now = timezone.now()
        qs = Subscription.objects.filter(
            status='active',
            starts_at__lte=now,
            expires_at__gte=now
        )
        serializer = SubscriptionSerializer(qs, many=True)
        return Response(serializer.data)


class TaxConfigViewSet(viewsets.ModelViewSet):
    queryset = TaxConfig.objects.all()
    serializer_class = TaxConfigSerializer

    def get_queryset(self):
        restaurant_id = self.request.query_params.get('restaurant_id')
        if restaurant_id:
            return TaxConfig.objects.filter(restaurant_id=restaurant_id, is_active=True)
        return super().get_queryset()