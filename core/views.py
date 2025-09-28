from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils.text import slugify

from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Product, Order, CartItem
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    OrderSerializer,
    UserRegistrationSerializer,
    CartItemSerializer,
)
from .tasks import send_order_confirmation
  
def index(request):
    return render(request, 'index.html')

def login_view(request):
    return render(request, 'login.html')

def products_view(request):
    return render(request, 'products.html')


# --- Custom Permissions ---
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Read: open to everyone.
    Write: only for admin users.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  
            return True
        return request.user and request.user.is_staff


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Users can access their own orders.
    Admins can access all orders.
    """
    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user or request.user.is_staff


# --- ViewSets ---
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(slug=slugify(serializer.validated_data['name']))


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']
    filterset_fields = ['category', 'is_active']

    def perform_create(self, serializer):
        serializer.save(slug=slugify(serializer.validated_data['name']))


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().select_related("customer").prefetch_related("items")
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["customer__username", "status"]
    ordering_fields = ["created_at", "total_price"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """
        Restrict non-admin users to see only their own orders.
        """
        user = self.request.user
        if user.is_staff:
            return Order.objects.all().select_related("customer").prefetch_related("items")
        return Order.objects.filter(customer=user).select_related("customer").prefetch_related("items")

    def perform_create(self, serializer):
        # Automatically assign logged-in user as the customer
        order = serializer.save(customer=self.request.user)

        # Trigger Celery task (make sure function name matches in tasks.py)
        send_order_confirmation.delay(order.id)


# --- User Registration ---
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


# --- Login (JWT) ---
# This is handled by TokenObtainPairView in urls.py, no custom view needed
# But if you want a custom response:
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Returns JWT access and refresh tokens
    """
    pass


# --- Add to Cart View ---
class AddToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "Product added to cart", "cart": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
