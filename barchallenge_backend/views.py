from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from decimal import Decimal
from .models import Beer, Order, Payment
from .serializers import BeerSerializer, OrderSerializer, PaymentSerializer

class BeerViewSet(viewsets.ModelViewSet):
    queryset = Beer.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = BeerSerializer

    def get_object(self, beer_id):
        try:
            return Beer.objects.get(id=beer_id)
        except Beer.DoesNotExist:
            return Response({'error': 'Beer not available!'}, status=status.HTTP_400_BAD_REQUEST)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = OrderSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        # Obtener el pedido y el monto del pago del cuerpo de la solicitud
        order_id = request.data.get('order')
        amount = Decimal(request.data.get('amount'))

        # Obtener la orden y calcular el monto total de la orden
        order = Order.objects.get(pk=order_id)
        total_amount = order.beer.price * order.quantity

        # Validar que el monto del pago sea válido
        if not 0 < float(amount) <= total_amount:
            return Response({'error': 'Invalid payment amount'}, status=status.HTTP_400_BAD_REQUEST)

        # Crear el pago y restar el monto del pago al total de la orden
        friend = request.data.get('friend', 'Unknown Friend')
        payment = Payment.objects.create(order=order, friend=friend, amount=amount)

        order = Order.objects.get(pk=order_id)
        order.total_amount -= amount

        order.save()
        

        # Devolver la respuesta con los detalles del pago
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)