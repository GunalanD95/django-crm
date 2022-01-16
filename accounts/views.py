from itertools import product
from django.shortcuts import render
from .models import Product, Customer , ProductTag , SaleOrder
# Create your views here.

def home(request):
    orders = SaleOrder.objects.all()
    customers = Customer.objects.all()
    total_orders = orders.count()
    total_customers = customers.count()
    invoiced = SaleOrder.objects.filter(status='invoiced').count()
    context = {
        'orders': orders,
        'customers': customers,
        'total_orders': total_orders,
        'total_customers': total_customers,
        'invoiced': invoiced
    }
    return render(request, 'accounts/home.html',context)


def products(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'accounts/products.html',context)

def customers(request):
    customers = Customer.objects.all()
    context = {
        'customers': customers
    }
    return render(request, 'accounts/customers.html',context)


def customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    #saleorder_set = SaleOrder.objects.filter(sale_order_customer=customer)
    saleorder = SaleOrder.objects.all()
    orders = customer.saleorder_set.all() # this is the same as above
    order_count = orders.count()
    context = {
        'customer': customer,
        'order_count': order_count,
        'orders': orders,
    }
    return render(request, 'accounts/customer.html',context)


def total_orders(request):
    orders = SaleOrder.objects.all()
    context = {
        'orders': orders
    }
    return render(request, 'accounts/orders.html',context)

def create_customer(request):
    return render(request, 'accounts/create_customer.html')


def create_order(request):
    return render(request, 'accounts/create_order.html')
