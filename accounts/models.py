from itertools import product
from sre_parse import CATEGORIES
from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    customer_user = models.OneToOneField(User, on_delete=models.SET_NULL, null= True)
    customer_pic = models.ImageField(upload_to='customer_pics/', blank=True)
    customer_name = models.CharField(max_length=50, null= True)
    customer_email = models.CharField(max_length=200 , null= True)
    customer_mobile = models.CharField(max_length=50 , null= True)
    date_created = models.DateTimeField(auto_now_add=True , null= True)


    def __str__(self):
        return self.customer_name

class ProductTag(models.Model):
    product_tag = models.CharField(max_length=200, null= True)

    def __str__(self):
        return self.product_tag


class Product(models.Model):

    CATEGORIES = (
        ('service', 'Service'),      
        ('stockable', 'Stockable'),
    )
    product_name = models.CharField(max_length=200, null= True)
    product_price = models.FloatField(null= True)
    product_category = models.CharField(max_length=200, null= True , choices=CATEGORIES)
    product_description = models.CharField(max_length=200, null= True)
    date_created = models.DateTimeField(auto_now_add=True , null= True)
    product_tag = models.ManyToManyField(ProductTag ,blank=True, null=True)


    def __str__(self):
        return self.product_name




class SaleOrder(models.Model):
    STATUS = (
        ('quotation', 'Quotation'),      
        ('ordered', 'Ordered'),
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('invoiced', 'Invoiced'),
    )
    sale_order_referencenumber = models.CharField(max_length=200, null= True)
    sale_order_customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null= True) # added a realtionship between the two models
    sale_order_product =  models.ForeignKey(Product, on_delete=models.SET_NULL, null= True)
    sale_order_quantity = models.IntegerField(null= True)
    sale_order_total_price = models.FloatField(null= True)
    sale_order_unit_price = models.FloatField(null= True)
    status = models.CharField(max_length=200, null= True , choices=STATUS, default='quotation')
    sale_order_date = models.DateTimeField(auto_now_add=True , null= True)

    def __str__(self):
        return self.sale_order_referencenumber