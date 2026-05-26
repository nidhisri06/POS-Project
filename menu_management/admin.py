from django.contrib import admin
from .models import MenuCategory, MenuItem, ModifierGroup, Modifier

admin.site.register(MenuCategory)
admin.site.register(MenuItem)
admin.site.register(ModifierGroup)
admin.site.register(Modifier)