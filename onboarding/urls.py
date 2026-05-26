from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, BranchViewSet, SubscriptionViewSet, TaxConfigViewSet

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'branches', BranchViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'tax-configs', TaxConfigViewSet)

urlpatterns = [
    path('', include(router.urls)),
]