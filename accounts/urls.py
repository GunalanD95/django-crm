from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path('',views.home, name='home'),
    path('customers/', views.customers, name='customers'),
    path('products/', views.products, name='products'),
    path('orders/', views.total_orders, name='orders'),
    path('<int:customer_id>/', views.customer, name='customer'),
    path('update_product/<int:product_id>/', views.update_product, name='update_product'),
    path('create_customer/', views.create_customer, name='create_customer'),
    path('create_order/', views.create_order, name='create_order'),
    path('create_product/', views.create_product, name='create_product'),
    path('update_order/<int:order_id>/', views.update_order, name='update_order'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('delete_customer/<int:customer_id>/', views.delete_customer, name='delete_customer'),
    path('edit/<int:customer_id>/', views.update_customer, name='update_customer'),
    path('<int:customer_id>/create_cu_order/', views.create_cu_order, name='create_cu_order'),
    path('user/',views.userPage, name='userPage'),
]