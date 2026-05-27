from django.db import models
from onboarding.models import Branch


class MenuCategory(models.Model):
    id = models.AutoField(primary_key=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="menu_categories")
    name = models.CharField(max_length=255)
    image_url = models.URLField(null=True, blank=True)
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    available_from = models.TimeField(null=True, blank=True)
    available_to = models.TimeField(null=True, blank=True)

    class Meta:
        db_table = 'menu_categories'
        ordering = ['sort_order']

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_veg = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    prep_time_mins = models.IntegerField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    nutritional_info = models.JSONField(default=dict, blank=True)
    allergen_info = models.JSONField(default=list, blank=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        db_table = 'menu_items'
        ordering = ['sort_order']

    def __str__(self):
        return self.name


class ModifierGroup(models.Model):
    id = models.AutoField(primary_key=True)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name="modifier_groups")
    name = models.CharField(max_length=255)
    is_required = models.BooleanField(default=False)
    min_select = models.IntegerField(default=0)
    max_select = models.IntegerField(default=1)

    class Meta:
        db_table = 'modifier_groups'

    def __str__(self):
        return f"{self.menu_item.name} - {self.name}"


class Modifier(models.Model):
    id = models.AutoField(primary_key=True)
    modifier_group = models.ForeignKey(ModifierGroup, on_delete=models.CASCADE, related_name="modifiers")
    name = models.CharField(max_length=255)
    extra_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_available = models.BooleanField(default=True)

    class Meta:
        db_table = 'modifiers'

    def __str__(self):
        return self.name
    
class ComboMeal(models.Model):
    branch = models.ForeignKey('onboarding.Branch', on_delete=models.CASCADE, related_name='combos')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    combo_price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    valid_from = models.DateField(null=True, blank=True)
    valid_until = models.DateField(null=True, blank=True)
    items = models.ManyToManyField(MenuItem, related_name='combos', blank=True)

    class Meta:
        db_table = 'combo_meals'

    def __str__(self):
        return self.name


class BranchMenuPrice(models.Model):
    branch = models.ForeignKey('onboarding.Branch', on_delete=models.CASCADE, related_name='branch_prices')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='branch_prices')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    class Meta:
        db_table = 'branch_menu_prices'
        unique_together = ('branch', 'menu_item')

    def __str__(self):
        return f"{self.branch.name} - {self.menu_item.name}: {self.price}"