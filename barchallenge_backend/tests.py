from django.test import TestCase

# Create your tests here.

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Beer, Order, Payment
from .serializers import PaymentSerializer

class PaymentViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Crear datos de prueba
        self.beer = Beer.objects.create(name='Test Beer', price=5.00)
        self.order = Order.objects.create(beer=self.beer, quantity=2, total_amount=10.00)

    def test_create_payment_valid(self):
        url = reverse('payment-list')
        data = {
            'order': self.order.id,
            'friend': 'John Doe',
            'amount': 8.00,
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verificar que el pago fue creado correctamente en la base de datos
        payment = Payment.objects.get(id=response.data['id'])
        self.assertEqual(payment.order, self.order)
        self.assertEqual(payment.friend, 'John Doe')
        self.assertEqual(payment.amount, 8.00)

    def test_create_payment_invalid_amount(self):
        url = reverse('payment-list')
        data = {
            'order': self.order.id,
            'friend': 'Jane Doe',
            'amount': 12.00,  # Este monto es mayor al total de la orden
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Invalid payment amount'})

        # Verificar que no se creó ningún pago en la base de datos
        self.assertEqual(Payment.objects.count(), 0)