from itertools import product
from multiprocessing import context
from unicodedata import category
from django.shortcuts import render
from .models import Product, Customer , ProductTag , SaleOrder
# Create your views here.
from .forms import OrderForm
from django.db.models import Q
from django.shortcuts import redirect
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users , admin_only


# @unauthenticated_user
@admin_only
def home(request):
    orders = SaleOrder.objects.all()[0:10]
    tot_orders = SaleOrder.objects.all()
    tot_cus = Customer.objects.all()
    customers = Customer.objects.all()[0:10]
    total_orders = tot_orders.count()
    total_customers = tot_cus.count()
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
    my_filter = OrderFilter(request.GET,queryset=orders)
    orders = my_filter.qs
    context = {
        'orders': orders,
        'filter': my_filter,
    }
    return render(request, 'accounts/orders.html',context)



@allowed_users(allowed_roles=['admin'])
@admin_only
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
    return render(request, 'accounts/create_customer.html')

# @allowed_users(allowed_roles=['admin'])
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
        sale_order_unit_price = request.POST.get('sale_order_unit_price')
        status = request.POST.get('status')
        sale_order = SaleOrder(sale_order_referencenumber= ref_no,sale_order_unit_price=sale_order_unit_price,sale_order_customer=customer, sale_order_product=product, sale_order_quantity=quantity, sale_order_total_price=total_price, status=status)
        sale_order.save()
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
        return redirect('/')

    return render(request, 'accounts/create_order.html',context)


@allowed_users(allowed_roles=['admin'])
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
        unit_price = request.POST.get('sale_order_unit_price')
        status = request.POST.get('status')
        order.sale_order_referencenumber= ref_no
        order.sale_order_customer=customer
        order.sale_order_product=product
        order.sale_order_quantity=quantity
        order.sale_order_total_price=total_price
        order.sale_order_unit_price=unit_price
        order.status=status
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
        return redirect('/')

    return render(request, 'accounts/update_order.html',context)




@allowed_users(allowed_roles=['admin'])
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

@allowed_users(allowed_roles=['admin'])
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
        prod.product_tag.remove(product_tag)
        prod.product_name=product_name
        prod.product_price=product_price
        prod.product_description=product_description
        p_tag = ProductTag.objects.get(id=request.POST.get('product_tag'))
        prod.product_tag.add(p_tag)
        prod.save()
        return redirect('products')

    return render(request, 'accounts/update_product.html',context)

@allowed_users(allowed_roles=['admin'])
def delete_order(request, order_id):
    order = SaleOrder.objects.get(id=order_id)
    if request.method == 'POST':
        if "cancel" in request.POST:
            print("request.POST:", request.POST)
            return redirect('home')
        else:
            order = SaleOrder.objects.get(id=order_id)
            order.delete()
            return redirect('home')
    context = {
        'order': order,
    }
    return render(request, 'accounts/delete_order.html',context)

@allowed_users(allowed_roles=['admin'])
def delete_product(request,product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        if "cancel" in request.POST:
            print("request.POST:", request.POST)
            return redirect('products')
        else:
            product = Product.objects.get(id=product_id)
            product.delete()
            return redirect('products')
    context = {
        'product': product,
    }
    return render(request, 'accounts/delete_product.html',context)

@allowed_users(allowed_roles=['admin'])
def delete_customer(request,customer_id):
    customer = Customer.objects.get(id=customer_id)
    if request.method == 'POST':
        if "cancel" in request.POST:
            print("request.POST:", request.POST)
            return redirect('customers')
        else:
            customer = Customer.objects.get(id=customer_id)
            customer.delete()
            return redirect('customers')
    context = {
        'customer': customer,
    }
    return render(request, 'accounts/delete_customer.html',context)

@allowed_users(allowed_roles=['admin'])
def update_customer(request,customer_id):

    if request.method == 'POST':
        print("IN POST METHOD")
        print("request.POST:", request.POST)
        customer = Customer.objects.get(id=customer_id)
        customer_name = request.POST.get('customer_names')
        customer_phone = request.POST.get('customer_phones')
        customer_email = request.POST.get('customer_emails')
        customer.customer_name=customer_name
        customer.customer_phone=customer_phone
        customer.customer_email=customer_email
        customer.save()
        return redirect('customers')
    elif request.method == 'GET':
        print("IN GET METHOD")
        customer = Customer.objects.get(id=customer_id)
        saleorder = SaleOrder.objects.all()
        orders = customer.saleorder_set.all() # this is the same as above
        order_count = orders.count()
        context = {
            'customer': customer,
            'order_count': order_count,
            'orders': orders,
        }
        return render(request, 'accounts/update_customer.html',context)

@allowed_users(allowed_roles=['admin'])
def create_cu_order(request,customer_id):
    customer = Customer.objects.get(pk=customer_id)
    products = Product.objects.all()
    if request.method == 'POST':
        sale_ref  = request.POST.get('sale_order_referencenumber')
        cus = Customer.objects.get(id=request.POST.get('sale_order_customer'))
        prod = Product.objects.get(id=request.POST.get('sale_order_product'))
        unit_price = request.POST.get('sale_order_unit_price')
        quantity = request.POST.get('sale_order_quantity')
        total_price = request.POST.get('sale_order_total_price')
        status = request.POST.get('status')
        order = SaleOrder(sale_order_referencenumber=sale_ref, sale_order_customer=cus, sale_order_product=prod, sale_order_unit_price=unit_price, sale_order_quantity=quantity, sale_order_total_price=total_price,status=status)
        order.save()
        return redirect('customer',customer_id)
    context = {
        'customer': customer,
        'products': products,
    }
    return render(request, 'accounts/customer_order.html',context) 


@allowed_users(allowed_roles=['customer'])
def userPage(request):
    customer_user = request.user.id
    customer = Customer.objects.get(customer_user=customer_user)
    orders = customer.saleorder_set.all()[0:10]
    tot_orders = customer.saleorder_set.all()
    total_orders = tot_orders.count()
    invoiced = tot_orders.filter(status='invoiced').count()
    delivered = tot_orders.filter(status='delivered').count()
    # print("customer",customer)
    # print("orders",orders)

    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': total_orders,
        'invoiced': invoiced,
        'delivered': delivered,
    }
    return render(request,'accounts/user.html',context)
