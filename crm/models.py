from django.db import models
from onboarding.models import Restaurant, Branch


class Customer(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='customers')
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    birthdate = models.DateField(null=True, blank=True)
    anniversary = models.DateField(null=True, blank=True)
    preferred_items = models.TextField(blank=True)  # comma-separated item names
    loyalty_points = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('restaurant', 'mobile')

    def __str__(self):
        return f"{self.name} - {self.mobile}"


class MembershipPlan(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='membership_plans')
    name = models.CharField(max_length=100)   # e.g. Silver, Gold, Platinum
    min_points = models.IntegerField(default=0)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    benefits = models.TextField(blank=True)

    def __str__(self):
        return f"{self.restaurant.restaurant_name} - {self.name}"


class CustomerMembership(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='membership')
    plan = models.ForeignKey(MembershipPlan, on_delete=models.SET_NULL, null=True)
    joined_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.customer.name} - {self.plan.name if self.plan else 'No Plan'}"


class LoyaltyTransaction(models.Model):
    TRANSACTION_TYPE = [
        ('earn', 'Earned'),
        ('redeem', 'Redeemed'),
        ('expire', 'Expired'),
        ('bonus', 'Bonus'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loyalty_transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE)
    points = models.IntegerField()
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - {self.transaction_type} - {self.points} pts"


class CustomerOrderHistory(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='order_history')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    order_number = models.CharField(max_length=50)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    points_earned = models.IntegerField(default=0)
    points_redeemed = models.IntegerField(default=0)
    items_summary = models.TextField(blank=True)  # JSON string of ordered items

    def __str__(self):
        return f"Order {self.order_number} - {self.customer.name}"


class Campaign(models.Model):
    CAMPAIGN_TYPE = [
        ('sms', 'SMS'),
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
    ]
    CAMPAIGN_STATUS = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('sent', 'Sent'),
        ('cancelled', 'Cancelled'),
    ]
    CAMPAIGN_TRIGGER = [
        ('manual', 'Manual'),
        ('birthday', 'Birthday'),
        ('anniversary', 'Anniversary'),
        ('inactive', 'Inactive Customer'),
        ('points', 'Points Milestone'),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='campaigns')
    name = models.CharField(max_length=255)
    campaign_type = models.CharField(max_length=20, choices=CAMPAIGN_TYPE)
    trigger = models.CharField(max_length=20, choices=CAMPAIGN_TRIGGER, default='manual')
    status = models.CharField(max_length=20, choices=CAMPAIGN_STATUS, default='draft')
    message = models.TextField()
    scheduled_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    target_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.campaign_type})"


class CustomerFeedback(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedbacks')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='feedbacks')
    order_number = models.CharField(max_length=50, blank=True)
    rating = models.IntegerField(default=5)          # 1 to 5
    food_rating = models.IntegerField(default=5)
    service_rating = models.IntegerField(default=5)
    ambience_rating = models.IntegerField(default=5)
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.customer.name if self.customer else 'Guest'} - {self.rating}★"


class PersonalizedOffer(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='offers')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='offers', null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    min_order_value = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    valid_from = models.DateField(null=True, blank=True)
    valid_until = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title