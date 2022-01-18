from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path('',views.home, name='home'),
    path('customers/', views.customers, name='customers'),
    path('products/', views.products, name='products'),
    path('orders/', views.total_orders, name='orders'),
    path('<int:customer_id>/', views.customer, name='customer'),
    path('create_customer/', views.create_customer, name='create_customer'),
    path('create_order/', views.create_order, name='create_order'),
    path('create_product/', views.create_product, name='create_product'),
    path('update_order/<int:order_id>/', views.update_order, name='update_order'),
    path('delete/<int:order_id>/', views.delete_order, name='delete_order'),
]