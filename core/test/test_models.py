from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Category, Product, Order, OrderItem

User = get_user_model()


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.product = Product.objects.create(
            name="Laptop",
            slug="laptop",
            price=1000,
            stock=5,
            category=self.category,
        )

    def test_order_total_updates_correctly(self):
        order = Order.objects.create(customer=self.user)
        OrderItem.objects.create(order=order, product=self.product, quantity=2)
        order.update_total()
        self.assertEqual(order.total_price, 2000)

    def test_orderitem_sets_price_from_product(self):
        order = Order.objects.create(customer=self.user)
        item = OrderItem.objects.create(order=order, product=self.product, quantity=1)
        self.assertEqual(item.price, self.product.price)

    def test_category_str(self):
        self.assertEqual(str(self.category), "Electronics")

    def test_product_str(self):
        self.assertEqual(str(self.product), "Laptop")

    def test_order_str(self):
        order = Order.objects.create(customer=self.user)
        self.assertIn("Order", str(order))

    def test_orderitem_str(self):
        order = Order.objects.create(customer=self.user)
        item = OrderItem.objects.create(order=order, product=self.product, quantity=3)
        self.assertIn("3 x Laptop", str(item))
