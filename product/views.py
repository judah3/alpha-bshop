from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from account import serializers
from product.models import Order, OrderItem, Product
from account.models import UserProfile
from product.serializers import ProductSerializer, OrderItemSerializer, OrderSerializer, OrderProductSerializer
# Create your views here.

@api_view(['GET'])
def productList(request):
    product_list = Product.objects.all()
    serializer = ProductSerializer(product_list, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def productDetails(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['POST'])
def createProduct(request):
    
    serializer = ProductSerializer(data=request.data) 
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
            
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'PUT'])
def updateProduct(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProductSerializer(product, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteProduct(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "DELETE":
        operation = product.delete()
        data = {}
        if operation:
            data['success'] = "Delete Successful"
        else:
            data['failure'] = "Failed to Delete"
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
def searchProduct(request):
    search = Product.objects.all().filter(name__icontains=request.data.get('search'))
    serializer = ProductSerializer(search, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createOrder(request):
    data = {
        'customer': request.data.get('user_id')
    }
    serializer = OrderSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

def check_product(product, quantity):
    if product.exists():
        new_quantity = int(product[0].quantity) + int(quantity)
    else:
        new_quantity = quantity
    return new_quantity

@api_view(['POST'])
def addToOrder(request, order_uuid):
    
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity')

    product = OrderItem.objects.filter(order = order_uuid).filter(product = product_id)

    data = {
        'order': order_uuid,
        'product':  request.data.get('product_id'),
        'quantity': check_product(product, quantity)
    }
    if product.exists():
        new_product = OrderItem.objects.get(order_item = product[0].order_item)
        new_product.delete()

    serializer = OrderItemSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def orderDetail(request, order_uuid):

    orderItem = OrderItem.objects.filter(order=order_uuid).select_related('order')
    orderItemSerializer = OrderProductSerializer(orderItem, many=True)

    return Response(orderItemSerializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def orderList(request, user_id):
    order_list = Order.objects.filter(customer = user_id)
    serializer = OrderSerializer(order_list, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
def deleteOrder(request, order_uuid):
    try:
        order = Order.objects.get(uuid=order_uuid)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "DELETE":
        operation = order.delete()
        data = {}
        if operation:
            data['success'] = "Delete Successful"
        else:
            data['failure'] = "Failed to Delete"
    return Response(data=data, status=status.HTTP_200_OK)