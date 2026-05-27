from django.contrib import admin
from .models import MenuCategory, MenuItem, ModifierGroup, Modifier,ComboMeal, BranchMenuPrice


admin.site.register(MenuCategory)
admin.site.register(MenuItem)
admin.site.register(ModifierGroup)
admin.site.register(Modifier)
admin.site.register(ComboMeal)
admin.site.register(BranchMenuPrice)