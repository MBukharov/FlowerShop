from django.db import models
from users.models import CustomUser
# Create your models here.

class Flower(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название товара")
    description = models.TextField(verbose_name="Описание")
    price = models.FloatField(verbose_name="Цена")
    quantity = models.IntegerField(verbose_name="Доступно к заказу")
    picture = models.ImageField(upload_to = 'catalog/static/catalog/img', verbose_name="Изображение")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Цветок"
        verbose_name_plural = "Цветы"



class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Flower, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"