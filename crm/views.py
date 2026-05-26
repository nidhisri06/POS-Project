from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import (
    Customer, MembershipPlan, CustomerMembership,
    LoyaltyTransaction, CustomerOrderHistory,
    Campaign, CustomerFeedback, PersonalizedOffer
)
from .serializers import (
    CustomerSerializer, CustomerDetailSerializer,
    MembershipPlanSerializer, CustomerMembershipSerializer,
    LoyaltyTransactionSerializer, CustomerOrderHistorySerializer,
    CampaignSerializer, CustomerFeedbackSerializer, PersonalizedOfferSerializer
)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'mobile', 'email']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CustomerDetailSerializer
        return CustomerSerializer

    def get_queryset(self):
        qs = Customer.objects.all()
        restaurant_id = self.request.query_params.get('restaurant_id')
        if restaurant_id:
            qs = qs.filter(restaurant_id=restaurant_id)
        return qs

    @action(detail=True, methods=['post'], url_path='add-points')
    def add_points(self, request, pk=None):
        customer = self.get_object()
        points = int(request.data.get('points', 0))
        description = request.data.get('description', 'Points added')

        if points <= 0:
            return Response({'error': 'Points must be greater than 0'}, status=400)

        customer.loyalty_points += points
        customer.save()

        LoyaltyTransaction.objects.create(
            customer=customer,
            transaction_type='earn',
            points=points,
            description=description
        )
        return Response({'message': f'{points} points added', 'total_points': customer.loyalty_points})

    @action(detail=True, methods=['post'], url_path='redeem-points')
    def redeem_points(self, request, pk=None):
        customer = self.get_object()
        points = int(request.data.get('points', 0))
        description = request.data.get('description', 'Points redeemed')

        if points <= 0:
            return Response({'error': 'Points must be greater than 0'}, status=400)
        if customer.loyalty_points < points:
            return Response({'error': 'Insufficient points'}, status=400)

        customer.loyalty_points -= points
        customer.save()

        LoyaltyTransaction.objects.create(
            customer=customer,
            transaction_type='redeem',
            points=points,
            description=description
        )
        return Response({'message': f'{points} points redeemed', 'remaining_points': customer.loyalty_points})

    @action(detail=False, methods=['get'], url_path='birthday-today')
    def birthday_today(self, request):
        today = timezone.now().date()
        customers = Customer.objects.filter(
            birthdate__month=today.month,
            birthdate__day=today.day
        )
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)


class MembershipPlanViewSet(viewsets.ModelViewSet):
    queryset = MembershipPlan.objects.all()
    serializer_class = MembershipPlanSerializer

    def get_queryset(self):
        restaurant_id = self.request.query_params.get('restaurant_id')
        if restaurant_id:
            return MembershipPlan.objects.filter(restaurant_id=restaurant_id)
        return super().get_queryset()


class CustomerMembershipViewSet(viewsets.ModelViewSet):
    queryset = CustomerMembership.objects.all()
    serializer_class = CustomerMembershipSerializer


class LoyaltyTransactionViewSet(viewsets.ModelViewSet):
    queryset = LoyaltyTransaction.objects.all()
    serializer_class = LoyaltyTransactionSerializer

    def get_queryset(self):
        customer_id = self.request.query_params.get('customer_id')
        if customer_id:
            return LoyaltyTransaction.objects.filter(customer_id=customer_id)
        return super().get_queryset()


class CustomerOrderHistoryViewSet(viewsets.ModelViewSet):
    queryset = CustomerOrderHistory.objects.all()
    serializer_class = CustomerOrderHistorySerializer

    def get_queryset(self):
        customer_id = self.request.query_params.get('customer_id')
        if customer_id:
            return CustomerOrderHistory.objects.filter(customer_id=customer_id)
        return super().get_queryset()


class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

    def get_queryset(self):
        restaurant_id = self.request.query_params.get('restaurant_id')
        if restaurant_id:
            return Campaign.objects.filter(restaurant_id=restaurant_id)
        return super().get_queryset()

    @action(detail=True, methods=['post'], url_path='send')
    def send_campaign(self, request, pk=None):
        campaign = self.get_object()
        # Placeholder — wire up SMS/Email/WhatsApp gateway here later
        campaign.status = 'sent'
        campaign.sent_at = timezone.now()
        campaign.save()
        return Response({'message': f'Campaign "{campaign.name}" marked as sent'})


class CustomerFeedbackViewSet(viewsets.ModelViewSet):
    queryset = CustomerFeedback.objects.all()
    serializer_class = CustomerFeedbackSerializer

    def get_queryset(self):
        branch_id = self.request.query_params.get('branch_id')
        if branch_id:
            return CustomerFeedback.objects.filter(branch_id=branch_id)
        return super().get_queryset()

    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        branch_id = request.query_params.get('branch_id')
        qs = CustomerFeedback.objects.all()
        if branch_id:
            qs = qs.filter(branch_id=branch_id)
        if not qs.exists():
            return Response({'message': 'No feedback found'})
        avg_rating = sum(f.rating for f in qs) / qs.count()
        return Response({
            'total_feedback': qs.count(),
            'average_rating': round(avg_rating, 2),
        })


class PersonalizedOfferViewSet(viewsets.ModelViewSet):
    queryset = PersonalizedOffer.objects.all()
    serializer_class = PersonalizedOfferSerializer

    def get_queryset(self):
        customer_id = self.request.query_params.get('customer_id')
        restaurant_id = self.request.query_params.get('restaurant_id')
        qs = PersonalizedOffer.objects.all()
        if customer_id:
            qs = qs.filter(customer_id=customer_id)
        if restaurant_id:
            qs = qs.filter(restaurant_id=restaurant_id)
        return qs