from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from .models import Beer, Order, Payment
from .serializers import BeerSerializer, OrderSerializer, PaymentSerializer

class BeerOrderPaymentTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_beers(self):
        response = self.client.get('/beers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order(self):
        beer = Beer.objects.create(name='Test Beer', price=Decimal('5.99'))
        data = {'beer': beer.id, 'quantity': 2}
        response = self.client.post('/orders/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_total_bill(self):
        beer = Beer.objects.create(name='Test Beer', price=Decimal('5.99'))
        order = Order.objects.create(beer=beer, quantity=2, total_amount=Decimal('11.98'))
        response = self.client.get('/orders/get_total_bill/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(round(response.data['total_bill'], 2)), str(round(float(order.total_amount), 2)))


    def test_pay_bill(self):
        beer = Beer.objects.create(name='Test Beer', price=Decimal('5.99'))
        order = Order.objects.create(beer=beer, quantity=2, total_amount=Decimal('11.98'))
        data = {'order': order.id, 'friend': 'Friend1', 'amount': Decimal('3.99')}
        response = self.client.post('/payments/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verificar que el pago se haya registrado correctamente
        payment = Payment.objects.get(order=order, friend='Friend1')
        self.assertEqual(payment.amount, Decimal('3.99'))

        # Verificar que el monto total de la orden se haya actualizado correctamente
        order.refresh_from_db()
        self.assertEqual(order.total_amount, Decimal('7.99'))  # 11.98 - 3.99