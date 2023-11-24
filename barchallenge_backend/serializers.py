from rest_framework import serializers
from .models import Beer, Order, Payment

class BeerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beer
        fields = '__all__'
        read_only_fields = ('created_at',)

class OrderSerializer(serializers.ModelSerializer):
    beer = BeerSerializer()  # Incluir la serialización de la cerveza
    class Meta:
        model = Order
        fields = ['id', 'beer', 'quantity', 'total_amount', 'created_at']
        read_only_fields = ('created_at',)

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('created_at',)