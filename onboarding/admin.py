from django.contrib import admin
from .models import Restaurant, Branch, Subscription, TaxConfig,StaffMember, RestaurantDocument, PaymentSetup

admin.site.register(Restaurant)
admin.site.register(Branch)
admin.site.register(Subscription)
admin.site.register(TaxConfig)
admin.site.register(StaffMember)
admin.site.register(RestaurantDocument)
admin.site.register(PaymentSetup)