from django.db import models
# Create your models here.

class Beer(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    # TODO: Posible implementacion con celery, en caso queramos calcular la orden x precio.
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     # se ha movido el import dentro del método save de la clase Order para evitar el problema de importación circular.
    #     from .tasks import calculate_and_update_bill
    #     calculate_and_update_bill.delay(self.id)


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    friend = models.CharField(max_length=255)  # Nombre del amigo que realiza el pago
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
