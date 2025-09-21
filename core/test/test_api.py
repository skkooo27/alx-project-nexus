from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from core.models import Category, Product, Order, OrderItem

User = get_user_model()


class ProductApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="apiuser", password="pass123")
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name="Books", slug="books")
        self.product = Product.objects.create(
            name="Django Book",
            slug="django-book",
            price=50,
            stock=10,
            category=self.category,
        )

    def test_list_products(self):
        url = reverse("product-list")  # DRF router
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_product(self):
        url = reverse("product-list")
        data = {
            "name": "New Book",
            "slug": "new-book",
            "price": 30,
            "stock": 5,
            "category": self.category.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)


class OrderApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="orderuser", password="pass123")
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name="Clothes", slug="clothes")
        self.product = Product.objects.create(
            name="T-Shirt",
            slug="t-shirt",
            price=20,
            stock=50,
            category=self.category,
        )

    def test_create_order(self):
        url = reverse("order-list")  # DRF router
        data = {
            "customer": self.user.id,
            "items": [
                {"product": self.product.id, "quantity": 2, "price": 20}
            ]
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.total_price, 40)

    def test_list_orders(self):
        Order.objects.create(customer=self.user, total_price=100)
        url = reverse("order-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
