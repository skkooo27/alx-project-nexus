from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, OrderViewSet, UserRegistrationView

# Create router and register viewsets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')

# Combine router URLs with custom endpoints
urlpatterns = [
    path('auth/register/', UserRegistrationView.as_view(), name='user-register'),
    path('', include(router.urls)),  # include router URLs
]
