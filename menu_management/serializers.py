from rest_framework import serializers
from .models import MenuCategory, MenuItem, ModifierGroup, Modifier
from .models import MenuCategory, MenuItem, ModifierGroup, Modifier, ComboMeal, BranchMenuPrice



class ModifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modifier
        fields = '__all__'


class ModifierGroupSerializer(serializers.ModelSerializer):
    modifiers = ModifierSerializer(many=True, read_only=True)

    class Meta:
        model = ModifierGroup
        fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):
    modifier_groups = ModifierGroupSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = MenuItem
        fields = '__all__'


class MenuItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class MenuCategorySerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = MenuCategory
        fields = '__all__'


class MenuCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = '__all__'



class ComboMealSerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = ComboMeal
        fields = '__all__'


class ComboMealCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComboMeal
        fields = '__all__'


class BranchMenuPriceSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='menu_item.name', read_only=True)

    class Meta:
        model = BranchMenuPrice
        fields = '__all__'