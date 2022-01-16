from django.forms import ModelForm
from .models import *

class OrderForm(ModelForm):
    class Meta:
        model = SaleOrder
        fields = ['sale_order_referencenumber', 'sale_order_customer', 'sale_order_product', 'sale_order_quantity', 'sale_order_total_price','status']