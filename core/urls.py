from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import (
    CategoryViewSet,
    ProductViewSet,
    OrderViewSet,
    UserRegistrationView,
    AddToCartView
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')

# Combine router URLs with custom endpoints
urlpatterns = [
    # Auth endpoints
    path('auth/register/', UserRegistrationView.as_view(), name='user-register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token-obtain-pair'),

    # Cart endpoint
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),

    # Include router URLs (products, categories, orders)
    path('', include(router.urls)),
]
