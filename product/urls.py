from django import views
from django.urls import path
from . import views


urlpatterns = [
    path('', views.productList, name='list'),
    path('detail/<int:id>/', views.productDetails, name='details'),
    path('create/', views.createProduct, name='create'),
    path('update/<int:id>', views.updateProduct, name='update'),
    path('delete/<int:id>', views.deleteProduct, name='delete'),
    path('search/', views.searchProduct, name='search'),

    # Order
    path('order/create', views.createOrder, name='order create'),
    path('order/<str:order_uuid>', views.addToOrder, name='add to order'),
    path('order/detail/<str:order_uuid>', views.orderDetail, name='order list'),
    
    
]