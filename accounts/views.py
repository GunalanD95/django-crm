from itertools import product
from django.shortcuts import render
from .models import Product, Customer , ProductTag , SaleOrder
# Create your views here.
from .forms import OrderForm


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

    if request.method == 'POST':
        print("request.POST:", request.POST)
        customer = Customer
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_mobile = request.POST.get('customer_mobile')
        customer_pic = request.FILES['customer_pic']
        cus = Customer(customer_name=customer_name, customer_email=customer_email, customer_mobile=customer_mobile, customer_pic=customer_pic)
        cus.save()
        return render(request, 'accounts/home.html') 
    return render(request, 'accounts/create_customer.html')


def create_order(request):
    customers = Customer.objects.all().order_by('id')
    products = Product.objects.all().order_by('id')
    sale_order = SaleOrder
    context = {
        'customers': customers,
        'products': products,
    }

    if request.method == 'POST':
        print("request.POST:", request.POST)
        print("PRODUCT", request.POST.get('sale_order_product'))
        print("CUSTOMER", request.POST.get('sale_order_customer'))
        customer = Customer.objects.get(id=request.POST.get('sale_order_customer'))
        product = Product.objects.get(id=request.POST.get('sale_order_product'))
        quantity = request.POST.get('sale_order_quantity')
        total_price = request.POST.get('sale_order_total_price')
        ref_no = request.POST.get('sale_order_referencenumber')
        sale_order = SaleOrder(sale_order_referencenumber= ref_no,sale_order_customer=customer, sale_order_product=product, sale_order_quantity=quantity, sale_order_total_price=total_price)
        sale_order.save()
        return render(request, 'accounts/home.html')

    return render(request, 'accounts/create_order.html',context)
