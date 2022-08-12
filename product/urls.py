from django import views
from django.urls import path
from . import views


urlpatterns = [
    path('product/', views.productList, name='list'),
    path('product/detail/<int:id>/', views.productDetails, name='details'),
    path('product/create/', views.createProduct, name='create'),
    path('product/update/<int:id>', views.updateProduct, name='update'),
    path('product/delete/<int:id>', views.deleteProduct, name='delete'),
    path('product/search/', views.searchProduct, name='search'),

    # Order
    path('order/create', views.createOrder, name='order create'),
    path('order/<str:order_uuid>', views.addToOrder, name='add to order'),
    path('order/detail/<str:order_uuid>', views.orderDetail, name='order list'),
    path('order/delete/<str:order_uuid>', views.deleteOrder, name='order list'),
    path('order/customer/<int:user_id>', views.orderList, name='order list'),
    
]