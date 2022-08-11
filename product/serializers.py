from rest_framework import serializers
from .models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'available', 'price', 'stock')

class ProductItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='product.name')
    description = serializers.CharField(source='product.description')
    price = serializers.CharField(source='product.price')

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'available', 'price')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductItemSerializer(source='*')
    
    class Meta:
        model = OrderItem
        fields = '__all__'