from django.db import models


class Restaurant(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20)
    gst_number = models.CharField(max_length=64, null=True, blank=True)
    pan_number = models.CharField(max_length=64, null=True, blank=True)
    fssai_number = models.CharField(max_length=64, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    cuisine_type = models.JSONField(default=list, blank=True)
    business_hours = models.JSONField(default=dict, blank=True)
    logo_url = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'restaurants'

    def __str__(self):
        return self.name


class Branch(models.Model):
    id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="branches")
    name = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'branches'

    def __str__(self):
        return f"{self.restaurant.name} - {self.name}"


class Subscription(models.Model):
    id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.CharField(max_length=64)
    status = models.CharField(max_length=32)
    starts_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    auto_renew = models.BooleanField(default=False)
    gateway_ref = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'subscriptions'

    def __str__(self):
        return f"{self.restaurant.name} - {self.plan}"


class TaxConfig(models.Model):
    id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="tax_configs")
    tax_name = models.CharField(max_length=255)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    applies_to = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'tax_configs'

    def __str__(self):
        return f"{self.tax_name} ({self.percentage}%)"
    
class StaffMember(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('cashier', 'Cashier'),
        ('waiter', 'Waiter'),
        ('kitchen', 'Kitchen Staff'),
    ]

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='staff')
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    joined_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'staff_members'

    def __str__(self):
        return f"{self.name} ({self.role})"


class RestaurantDocument(models.Model):
    DOC_TYPE_CHOICES = [
        ('gst', 'GST Certificate'),
        ('fssai', 'FSSAI License'),
        ('pan', 'PAN Card'),
        ('trade', 'Trade License'),
        ('other', 'Other'),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField(max_length=50, choices=DOC_TYPE_CHOICES)
    doc_number = models.CharField(max_length=100, blank=True)
    file_url = models.URLField(blank=True, null=True)
    expiry_date = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'restaurant_documents'

    def __str__(self):
        return f"{self.restaurant.name} - {self.doc_type}"


class PaymentSetup(models.Model):
    GATEWAY_CHOICES = [
        ('razorpay', 'Razorpay'),
        ('stripe', 'Stripe'),
        ('paytm', 'Paytm'),
        ('phonepe', 'PhonePe'),
        ('cash', 'Cash Only'),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='payment_setups')
    gateway = models.CharField(max_length=50, choices=GATEWAY_CHOICES)
    api_key = models.CharField(max_length=255, blank=True)
    api_secret = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payment_setups'

    def __str__(self):
        return f"{self.restaurant.name} - {self.gateway}"