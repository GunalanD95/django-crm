from itertools import product
from django.shortcuts import render
from .models import Product, Customer , ProductTag , SaleOrder
# Create your views here.

def home(request):
    orders = SaleOrder.objects.all()
    customers = Customer.objects.all()
    context = {
        'orders': orders,
        'customers': customers,
    }
    return render(request, 'accounts/home.html',context)


def products(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'accounts/products.html',context)

def customers(request):
    return render(request, 'accounts/customers.html')
