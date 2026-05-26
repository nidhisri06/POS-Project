from django.contrib import admin
from .models import (
    Customer, MembershipPlan, CustomerMembership,
    LoyaltyTransaction, CustomerOrderHistory,
    Campaign, CustomerFeedback, PersonalizedOffer
)

admin.site.register(Customer)
admin.site.register(MembershipPlan)
admin.site.register(CustomerMembership)
admin.site.register(LoyaltyTransaction)
admin.site.register(CustomerOrderHistory)
admin.site.register(Campaign)
admin.site.register(CustomerFeedback)
admin.site.register(PersonalizedOffer)