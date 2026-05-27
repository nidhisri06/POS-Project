from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RestaurantViewSet, BranchViewSet, SubscriptionViewSet, TaxConfigViewSet,
    StaffMemberViewSet, RestaurantDocumentViewSet, PaymentSetupViewSet
)

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'branches', BranchViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'tax-configs', TaxConfigViewSet)
router.register(r'staff', StaffMemberViewSet)
router.register(r'documents', RestaurantDocumentViewSet)
router.register(r'payment-setup', PaymentSetupViewSet)

urlpatterns = [
    path('', include(router.urls)),
]