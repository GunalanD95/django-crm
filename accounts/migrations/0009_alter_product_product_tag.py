# Generated by Django 4.0 on 2022-01-18 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_customer_customer_pic_alter_saleorder_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_tag',
            field=models.ManyToManyField(blank=True, null=True, to='accounts.ProductTag'),
        ),
    ]
