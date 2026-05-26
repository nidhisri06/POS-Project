from django.contrib import admin
from .models import Restaurant, Branch, Subscription, TaxConfig

admin.site.register(Restaurant)
admin.site.register(Branch)
admin.site.register(Subscription)
admin.site.register(TaxConfig)