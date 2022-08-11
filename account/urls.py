from django import views
from django.urls import path
from . import views
from .views import LoginAPI, customerList, customerDetail,searchCustomer
from knox import views as knox_views

urlpatterns = [
    path('register/', views.RegisterAPI.as_view(), name='Register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('customers/', customerList, name='user list'),
    path('customer/<int:id>', customerDetail, name='user details'),
    path('customer/search/s', searchCustomer, name='search customer'),
    
]