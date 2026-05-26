from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomerViewSet, MembershipPlanViewSet, CustomerMembershipViewSet,
    LoyaltyTransactionViewSet, CustomerOrderHistoryViewSet,
    CampaignViewSet, CustomerFeedbackViewSet, PersonalizedOfferViewSet
)

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'membership-plans', MembershipPlanViewSet)
router.register(r'memberships', CustomerMembershipViewSet)
router.register(r'loyalty-transactions', LoyaltyTransactionViewSet)
router.register(r'order-history', CustomerOrderHistoryViewSet)
router.register(r'campaigns', CampaignViewSet)
router.register(r'feedback', CustomerFeedbackViewSet)
router.register(r'offers', PersonalizedOfferViewSet)

urlpatterns = [
    path('', include(router.urls)),
]