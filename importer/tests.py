from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Product, Order

class ImporterViewsTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.client = Client()
        self.user = User.objects.create(
            user_name="testuser",
            full_name="Test User",
            email="testuser@example.com",
            phone="1234567890",
            user_type="customer"
        )
        self.admin = User.objects.create(
            user_name="adminuser",
            full_name="Admin User",
            email="admin@example.com",
            phone="0987654321",
            user_type="admin"
        )
        self.product = Product.objects.create(
            name="Test Product",
            price=100.00,
            description="Test Description",
            image_urls="http://example.com/image.jpg"
        )

    def test_register_view(self):
        response = self.client.post(reverse('register'), {
            'user_name': 'newuser',
            'full_name': 'New User',
            'email': 'newuser@example.com',
            'phone': '1112223333',
            'password': 'password123',
            'user_type': 'customer'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(User.objects.filter(user_name='newuser').exists())

    def test_login_view_customer(self):
        response = self.client.post(reverse('login'), {
            'user_name': self.user.user_name,
            'phone': self.user.phone,
            'login_type': 'customer'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to product_list
        self.assertEqual(self.client.session['user_id'], self.user.id)

    def test_login_view_admin(self):
        response = self.client.post(reverse('login'), {
            'user_name': self.admin.user_name,
            'phone': self.admin.phone,
            'login_type': 'admin'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to admin_dashboard
        self.assertEqual(self.client.session['user_id'], self.admin.id)

    def test_show_all_product(self):
        self.client.session['user_id'] = self.user.id
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_product_detail_post(self):
        self.client.session['user_id'] = self.user.id
        response = self.client.post(reverse('product_detail', args=[self.product.id]), {
            'quantity': 2,
            'buyer_phone': self.user.phone
        })
        self.assertEqual(response.status_code, 302)  # Redirect to product_list
        self.assertTrue(Order.objects.filter(product=self.product, buyer_phone=self.user.phone).exists())

    def test_logout_view(self):
        self.client.session['user_id'] = self.user.id
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertNotIn('user_id', self.client.session)

    def test_admin_dashboard_access_denied(self):
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, reverse('login'))

    def test_admin_dashboard_access_granted(self):
        self.client.session['user_id'] = self.admin.id
        self.client.session['login_type'] = 'admin'
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Users who didn't order")

    def test_order_history(self):
        Order.objects.create(
            product=self.product,
            quantity=1,
            buyer_phone=self.user.phone
        )
        self.client.session['user_id'] = self.user.id
        self.client.session['phone'] = self.user.phone
        response = self.client.get(reverse('order_history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)