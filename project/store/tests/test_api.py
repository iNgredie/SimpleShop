import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from store.models import StoreUser, Product, ShoppingCart
from store.serializers import ProductSerializer, ShoppingCartSerializer


def sample_product(**params):
    """Create and return a sample product"""
    defaults = {
        'vendor_code': 'keyboard123',
        'title': 'daskeyboard',
        'purchase_price': 40,
        'retail_price': 60
    }
    defaults.update(params)

    return Product.objects.create(**defaults)


class ProductApiTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='80kapaar1'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.user.save()

        self.product_1 = Product.objects.create(
            vendor_code='abc123',
            title='Test product 1',
            purchase_price='25',
            retail_price='26'
        )
        self.product_2 = Product.objects.create(
            vendor_code='abc567',
            title='Test product 2',
            purchase_price='30',
            retail_price='50'
        )
        self.product_3 = Product.objects.create(
            vendor_code='zxc123',
            title='Test product 3',
            purchase_price='40',
            retail_price='60'
        )

    def test_get_product(self):
        url = reverse('product-list')
        response = self.client.get(url)
        serializer_data = ProductSerializer(
            [self.product_1, self.product_2, self.product_3],
            many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(3, Product.objects.all().count())
        url = reverse('product-list')
        data = {
            'vendor_code': 'keyboard123',
            'title': 'daskeyboard',
            'purchase_price': '40',
            'retail_price': '60'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(
            url,
            data=json_data,
            content_type='application/json'
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Product.objects.all().count())

    def test_update(self):
        url = reverse('product-detail', args=(self.product_1.id,))
        data = {
            'vendor_code': self.product_1.vendor_code,
            'title': self.product_1.title,
            'purchase_price': '40',
            'retail_price': self.product_1.retail_price
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(
            url,
            data=json_data,
            content_type='application/json'
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.product_1.refresh_from_db()
        self.assertEqual(40, self.product_1.purchase_price)


class ShoppingCartApiTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='user1',
            email='user1@example.com',
            password='80kapaar1'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.product = sample_product()
        self.product.save()
        self.user.save()

        self.cart = ShoppingCart.objects.create(
            client=self.user,
            product=self.product,
            amount=10,
            price=26,
            total=260
        )
        # self.cart.refresh_from_db()

    def test_get_cart(self):
        url = reverse('shoppingcart-list')
        response = self.client.get(url)

        serializer_data = ShoppingCartSerializer([self.cart], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_update(self):
        url = reverse('shoppingcart-detail', args=(self.cart.id,))
        data = {
            'client': 'user',
            'product': self.cart.product.title,
            'amount': 10,
            'price': self.product.retail_price,
            'total': 600
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(
            url,
            data=json_data,
            content_type='application/json'
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.cart.refresh_from_db()
        self.assertEqual(10, self.cart.amount)
        self.assertEqual(600, self.cart.total)

    def test_update_not_client(self):
        self.user2 = get_user_model().objects.create_user(
            username='user2',
            email='user2@example.com',
            password='80kapaar1'
        )
        url = reverse('shoppingcart-detail', args=(self.cart.id,))
        data = {
            'client': 'user',
            'product': self.cart.product.title,
            'amount': 10,
            'price': self.product.retail_price,
            'total': 600
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(
            url,
            data=json_data,
            content_type='application/json'
        )
        print(self.user2)
        print(self.user)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.cart.refresh_from_db()
        self.assertEqual(10, self.cart.amount)
        self.assertEqual(600, self.cart.total)
