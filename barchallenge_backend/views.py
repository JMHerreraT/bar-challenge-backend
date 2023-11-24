from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from decimal import Decimal
from .models import Beer, Order, Payment
from .serializers import BeerSerializer, OrderSerializer, PaymentSerializer
from django.db.models import Sum
from rest_framework.decorators import action

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

    def create(self, request, *args, **kwargs):
        orders_data = request.data

        # Lista para almacenar los objetos de pedido creados
        created_orders = []

        for order_data in orders_data:
            quantity = order_data.get('quantity')
            beer_id = Decimal(order_data.get('beer'))

            beer = Beer.objects.get(pk=beer_id)

            order = Order.objects.create(beer=beer, quantity=quantity, total_amount=Decimal(beer.price) * Decimal(quantity))
            created_orders.append(order)

        serializer = OrderSerializer(created_orders, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    @action(detail=False, methods=['get'])
    def get_total_bill(self, request):
        total_bill = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum']
        return Response({'total_bill': total_bill}, status=status.HTTP_200_OK)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        order_id = request.data.get('order')
        amount = Decimal(request.data.get('amount'))

        order = Order.objects.get(pk=order_id)
        total_amount = order.beer.price * order.quantity

        if not 0 < float(amount) <= total_amount:
            return Response({'error': 'Invalid payment amount'}, status=status.HTTP_400_BAD_REQUEST)

        friend = request.data.get('friend', 'Unknown Friend')
        payment = Payment.objects.create(order=order, friend=friend, amount=amount)

        order.total_amount -= amount
        order.save()

        # # Dividir la cuenta entre los amigos
        # friends_count = Payment.objects.filter(order=order).values('friend').distinct().count()
        # if friends_count > 0:
        #     share_amount = order.total_amount / friends_count
        #     Payment.objects.filter(order=order).update(amount=share_amount)

        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)