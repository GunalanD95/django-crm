from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path('',views.home, name='home'),
    path('customers', views.customers, name='customers'),
    path('products', views.products, name='products'),
    path('<int:customer_id>/', views.customer, name='customer'),
]