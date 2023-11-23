from celery import shared_task
from .models import Order

@shared_task
def calculate_and_update_bill(order_id):
    order = Order.objects.get(pk=order_id)
    total_amount = order.beer.price * order.quantity
    order.total_amount = total_amount
    order.save()