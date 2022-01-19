from itertools import product
from multiprocessing import context
from unicodedata import category
from django.shortcuts import render
from .models import Product, Customer , ProductTag , SaleOrder
# Create your views here.
from .forms import OrderForm
from django.db.models import Q
from django.shortcuts import redirect


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
    for i in products:
        product_tag = i.product_tag.all()
        print("product_tag", product_tag)
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
        'invoiced': invoiced,
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
        return render(request, 'accounts/home.html',context)

    return render(request, 'accounts/create_order.html',context)

def update_order(request, order_id):
    order = SaleOrder.objects.get(id=order_id)
    customer = Customer.objects.get(id=order.sale_order_customer.id)
    product = Product.objects.get(id=order.sale_order_product.id)
    customers = Customer.objects.filter(~Q(id=customer.id))
    products = Product.objects.filter(~Q(id=product.id))
    context = {
        'order': order,
        'customer': customer,
        'product': product,
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
        order.sale_order_referencenumber= ref_no
        order.sale_order_customer=customer
        order.sale_order_product=product
        order.sale_order_quantity=quantity
        order.sale_order_total_price=total_price
        order.save()
        customers = Customer.objects.all().order_by('id')
        products = Product.objects.all().order_by('id')
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
            'invoiced': invoiced,
            'products': products,
        }
        return render(request, 'accounts/home.html',context)

    return render(request, 'accounts/update_order.html',context)





def create_product(request):
    product_tag = ProductTag.objects.all()
    products = Product.objects.all()
    context = {
        'product_tag': product_tag,
        'products': products,
    }
    if request.method == 'POST':
        print("request.POST:", request.POST)
        product = Product
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        product_description = request.POST.get('product_description')
        prod = Product.objects.create(product_name=product_name, product_price=product_price, product_description=product_description)
        p_tag = ProductTag.objects.get(id=request.POST.get('product_tag'))
        prod.product_tag.add(p_tag)
        # prod.save()
        return render(request, 'accounts/products.html',context) 
    return render(request, 'accounts/create_product.html',context)


def update_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product_tag = ProductTag.objects.get(id=product.product_tag.all()[0].id)
    product_tags = ProductTag.objects.filter(~Q(id=product_tag.id))
    context = {
        'product': product,
        'product_tag': product_tag,
        'product_tags': product_tags,
    }
    print("product_tag", product_tag)
    if request.method == 'POST':
        print("request.POST:", request.POST)
        product = Product
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        product_description = request.POST.get('product_description')
        prod = Product.objects.get(id=product_id)
        prod.product_name=product_name
        prod.product_price=product_price
        prod.product_description=product_description
        prod.save()
        return render(request, 'accounts/products.html',context)

    return render(request, 'accounts/update_product.html',context)


def delete_order(request, order_id):
    order = SaleOrder.objects.get(id=order_id)
    if request.method == 'POST':
        order = SaleOrder.objects.get(id=order_id)
        order.delete()
        return redirect('home')
    # order = SaleOrder.objects.get(id=order_id)
    # order.delete()
    # orders = SaleOrder.objects.all()
    # customers = Customer.objects.all()
    # total_orders = orders.count()
    # total_customers = customers.count()
    # invoiced = SaleOrder.objects.filter(status='invoiced').count()
    # context = {
    #     'orders': orders,
    #     'customers': customers,
    #     'total_orders': total_orders,
    #     'total_customers': total_customers,
    #     'invoiced': invoiced,
    #     'order': order,
    # }
    context = {
        'order': order,
    }
    return render(request, 'accounts/delete_order.html',context)
