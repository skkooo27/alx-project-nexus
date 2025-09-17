from django.utils.text import slugify
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters

from .models import Category, Product, Order
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(slug=slugify(serializer.validated_data['name']))


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
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
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["customer__username", "status"]
    ordering_fields = ["created_at", "total_price"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
