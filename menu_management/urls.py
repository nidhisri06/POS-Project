from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MenuCategoryViewSet, MenuItemViewSet,
    ModifierGroupViewSet, ModifierViewSet
)

router = DefaultRouter()
router.register(r'categories', MenuCategoryViewSet)
router.register(r'items', MenuItemViewSet)
router.register(r'modifier-groups', ModifierGroupViewSet)
router.register(r'modifiers', ModifierViewSet)

urlpatterns = [
    path('', include(router.urls)),
]