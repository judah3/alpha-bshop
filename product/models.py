from django.db import models
import uuid
from account.models import User
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    available = models.BooleanField(default=False)
    price = models.CharField(max_length=32)
    stock = models.IntegerField()

class Order(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="order")

class OrderItem(models.Model):
    order_item = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name="orderitem")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name="orderproduct")
    quantity = models.IntegerField()
    
class Image(models.Model):
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.name