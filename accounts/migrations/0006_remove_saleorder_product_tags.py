# Generated by Django 4.0 on 2022-01-14 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_saleorder_product_tags_remove_product_product_tag_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saleorder',
            name='product_tags',
        ),
    ]
