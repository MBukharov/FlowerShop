from django.db import models
from users.models import CustomUser
from catalog.models import Flower

# Create your models here.

class Order(models.Model):
    STATUS_CHOICES = [
        ('СБОРКА', 'На сборке'),
        ('В ПУТИ', 'В доставке'),
        ('ВЫПОЛННЕН', 'Выполнен'),
        ('ОТМЕНЕН', 'Отменен'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    products = models.ManyToManyField(Flower, through='OrderProduct')
    sum = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='СБОРКА')
    date = models.DateTimeField()

    def __str__(self):
        return f"Order {self.id} by {self.user.username} at {self.date}"


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Flower, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} x {self.quantity} for Order {self.order.id}"