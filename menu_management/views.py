from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import MenuCategory, MenuItem, ModifierGroup, Modifier
from .models import MenuCategory, MenuItem, ModifierGroup, Modifier, ComboMeal, BranchMenuPrice
from .serializers import (
    MenuCategorySerializer, MenuCategoryCreateSerializer,
    MenuItemSerializer, MenuItemCreateSerializer,
    ModifierGroupSerializer, ModifierSerializer
)


class MenuCategoryViewSet(viewsets.ModelViewSet):
    queryset = MenuCategory.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return MenuCategoryCreateSerializer
        return MenuCategorySerializer

    def get_queryset(self):
        branch_id = self.request.query_params.get('branch_id')
        if branch_id:
            return MenuCategory.objects.filter(
                branch_id=branch_id, is_active=True
            ).order_by('sort_order')
        return super().get_queryset()


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return MenuItemCreateSerializer
        return MenuItemSerializer

    def get_queryset(self):
        qs = MenuItem.objects.all()
        category_id = self.request.query_params.get('category_id')
        is_veg = self.request.query_params.get('is_veg')
        is_available = self.request.query_params.get('is_available')

        if category_id:
            qs = qs.filter(category_id=category_id)
        if is_veg is not None:
            qs = qs.filter(is_veg=is_veg == 'true')
        if is_available is not None:
            qs = qs.filter(is_available=is_available == 'true')
        return qs

    @action(detail=True, methods=['patch'], url_path='toggle-availability')
    def toggle_availability(self, request, pk=None):
        item = self.get_object()
        item.is_available = not item.is_available
        item.save()
        return Response({'is_available': item.is_available})


class ModifierGroupViewSet(viewsets.ModelViewSet):
    queryset = ModifierGroup.objects.all()
    serializer_class = ModifierGroupSerializer

    def get_queryset(self):
        menu_item_id = self.request.query_params.get('menu_item_id')
        if menu_item_id:
            return ModifierGroup.objects.filter(menu_item_id=menu_item_id)
        return super().get_queryset()


class ModifierViewSet(viewsets.ModelViewSet):
    queryset = Modifier.objects.all()
    serializer_class = ModifierSerializer

    def get_queryset(self):
        group_id = self.request.query_params.get('group_id')
        if group_id:
            return Modifier.objects.filter(modifier_group_id=group_id)
        return super().get_queryset()
    

from .serializers import (
    MenuCategorySerializer, MenuCategoryCreateSerializer,
    MenuItemSerializer, MenuItemCreateSerializer,
    ModifierGroupSerializer, ModifierSerializer,
    ComboMealSerializer, ComboMealCreateSerializer, BranchMenuPriceSerializer
)


class ComboMealViewSet(viewsets.ModelViewSet):
    queryset = ComboMeal.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ComboMealCreateSerializer
        return ComboMealSerializer

    def get_queryset(self):
        branch_id = self.request.query_params.get('branch_id')
        if branch_id:
            return ComboMeal.objects.filter(branch_id=branch_id)
        return super().get_queryset()


class BranchMenuPriceViewSet(viewsets.ModelViewSet):
    queryset = BranchMenuPrice.objects.all()
    serializer_class = BranchMenuPriceSerializer

    def get_queryset(self):
        branch_id = self.request.query_params.get('branch_id')
        if branch_id:
            return BranchMenuPrice.objects.filter(branch_id=branch_id)
        return super().get_queryset()